"""
Model our creature and wrap it in one class.
First version on 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

----------------------------------

Modified by Daniel Scrivener 09/2023
"""

from Component import Component
from Point import Point
import ColorType as Ct
from Shapes import Cube, Cylinder, Sphere, Cone
from Shapes import Cylinder
import numpy as np


class ModelLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature.
    #
    # In order to simplify the process of constructing your model, the rotational origin of each Shape has been offset by -1/2 * dz,
    # where dz is the total length of the shape along its z-axis. In other words, the rotational origin lies along the smallest
    # local z-value rather than being at the translational origin, or the object's true center.
    #
    # This allows Shapes to rotate "at the joint" when chained together, much like segments of a limb.
    #
    # In general, you should construct each component such that it is longest in its local z-direction:
    # otherwise, rotations may not behave as expected.
    #
    # Please see Blackboard for an illustration of how this behavior works.

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, display_obj=None):
        super().__init__(position, display_obj)
        self.contextParent = parent

        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural ways
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.

        abdomen = Sphere(Point((0, 0, 0)), shaderProg, size=[0.8, 0.8, 0.8], color=Ct.DARKORANGE2, limb=False)

        head = Sphere(Point((0, 0, -0.6)), shaderProg, size=[0.5, 0.5, 0.5], color=Ct.DARKORANGE1, limb=False)
        head.setRotateExtent(head.vAxis, -30, 30)
        head.setRotateExtent(head.uAxis, -30, 30)
        head.setRotateExtent(head.wAxis, -30, 30)
        abdomen.addChild(head)

        eye1 = Sphere(Point((0.08, 0.2, -0.4)), shaderProg, size=[0.08, 0.08, 0.05], color=Ct.WHITE, limb=False)
        eye2 = Sphere(Point((-0.08, 0.2, -0.4)), shaderProg, size=[0.08, 0.08, 0.05], color=Ct.WHITE, limb=False)
        eye1.setRotateExtent(eye1.uAxis, -25, 25)
        eye2.setRotateExtent(eye2.uAxis, -25, 25)
        eye1.setRotateExtent(eye1.vAxis, -25, 25)
        eye2.setRotateExtent(eye2.vAxis, -25, 25)
        eye1.setRotateExtent(eye1.wAxis, -25, 25)
        eye2.setRotateExtent(eye2.wAxis, -25, 25)

        pupil_offset = -0.04
        pupil_size = [0.04, 0.04, 0.03]

        pupil1 = Sphere(Point((0, 0, pupil_offset)), shaderProg, size=pupil_size, color=Ct.BLACK, limb=False)
        pupil2 = Sphere(Point((0, 0, pupil_offset)), shaderProg, size=pupil_size, color=Ct.BLACK, limb=False)

        eye1.addChild(pupil1)
        eye2.addChild(pupil2)

        fang1 = Cone(Point((0.04, 0.05, -0.55)), shaderProg, size=[0.02, 0.02, 0.1], color=Ct.RED, limb=False)
        fang2 = Cone(Point((-0.04, 0.05, -0.55)), shaderProg, size=[0.02, 0.02, 0.1], color=Ct.RED, limb=False)
        fang1.setRotateExtent(fang1.vAxis, -10, 10)
        fang2.setRotateExtent(fang2.vAxis, -10, 10)
        fang1.rotate(180, fang1.uAxis)
        fang2.rotate(180, fang2.uAxis)
        head.addChild(eye1)
        head.addChild(eye2)
        head.addChild(fang1)
        head.addChild(fang2)

        stripe1 = Cylinder(Point((0, 0, -0.15)), shaderProg, size=[0.74, 0.74, 0.07], color=Ct.BLACK, limb=False)
        stripe2 = Cylinder(Point((0, 0, 0.15)), shaderProg, size=[0.74, 0.74, 0.07], color=Ct.BLACK, limb=False)
        abdomen.addChild(stripe1)
        abdomen.addChild(stripe2)

        leg_groupLeft = Component(Point((0, 0.3, 0)))
        leg_groupRight = Component(Point((0, 0.3, 0)))
        abdomen.addChild(leg_groupLeft)
        abdomen.addChild(leg_groupRight)

        self.initial_leg_angles = []
        legs = []
        for i in range(4):
            leg = self.create_leg(shaderProg, Ct.DARKORANGE2, Ct.DARKORANGE3)
            angle = 20 + (i + 1) * 25
            leg.setCurrentAngle(angle, abdomen.uAxis)
            leg.setRotateExtent(leg.uAxis, angle - 10, angle + 10)
            legs.append(leg)
            self.initial_leg_angles.append(angle)
            leg_groupLeft.addChild(leg)

        for i in range(4, 8):
            leg = self.create_leg(shaderProg, Ct.DARKORANGE2, Ct.DARKORANGE3)
            angle = 340 - (i - 4 + 1) * 25
            leg.setCurrentAngle(angle, abdomen.uAxis)
            leg.setRotateExtent(leg.uAxis, angle - 10, angle + 10)
            legs.append(leg)
            self.initial_leg_angles.append(angle)
            leg_groupRight.addChild(leg)

        leg_groupLeft.rotate(60, leg_groupLeft.wAxis)
        leg_groupRight.rotate(120, leg_groupRight.wAxis)
        self.addChild(abdomen)
        self.components = [abdomen, head, eye1, eye2, fang1, fang2] + legs
        self.componentDict = {
            'head': head,
            'eye1': eye1,
            'eye2': eye2,
            'fang1': fang1,
            'fang2': fang2,
            **{f"leg{i + 1}_upper": legs[i] for i in range(8)}
        }

        self.componentList = self.components

        self.legs = legs
        self.abdomen = abdomen
        self.head = head
        self.eye1 = eye1
        self.eye2 = eye2
        self.fang1 = fang1
        self.fang2 = fang2

    def create_leg(self, shaderProg, color1, color2):
        upper_leg = Cylinder(Point((0.0, 0, 0.6)), shaderProg, [0.06, 0.06, 0.6], color=color1)
        upper_leg.setRotateExtent(upper_leg.vAxis, -30, 30)

        lower_leg = Cylinder(Point((0.0, 0, 0.3)), shaderProg, [0.05, 0.05, 1.2], color=color2)
        lower_leg.setRotateExtent(lower_leg.vAxis, -30, 30)



        upper_leg.addChild(lower_leg)
        return upper_leg

    def reset(self):
        super().reset()
        for leg, angle in zip(self.legs, self.initial_leg_angles):
            leg.reset()
            leg.setCurrentAngle(angle, self.abdomen.uAxis)

            self.head.reset()
            self.head.setCurrentAngle(0, self.head.vAxis)

            self.eye1.reset()
            self.eye2.reset()

            self.fang1.reset()
            self.fang2.reset()
            self.fang1.rotate(180, self.fang1.uAxis)
            self.fang2.rotate(180, self.fang2.uAxis)