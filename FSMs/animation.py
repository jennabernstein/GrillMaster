from . import AbstractGameFSM
from utils import magnitude, EPSILON, SpriteManager
from utils import EPSILON

from statemachine import State

class AnimateFSM(AbstractGameFSM):
    def on_enter_state(self):
        state = self.current_state.id
        if self.obj.row != self.obj.rowList[state]:
            self.obj.nFrames = self.obj.nFramesList[state]
            self.obj.frame = 0
            self.obj.row = self.obj.rowList[state]
            self.obj.framesPerSecond = self.obj.framesPerSecondList[state]
            self.obj.animationTimer = 0
            self.obj.image = SpriteManager.getInstance().getSprite(self.obj.imageName,
                                                                   (self.obj.frame, self.obj.row))


        self.obj.image = SpriteManager.getInstance().getSprite(
                self.obj.imageName, (self.obj.frame, self.obj.row), self.obj.scale
            )


class WalkingFSM(AnimateFSM):
    
    forward = State(initial=True)
    back = State()
    standingforward = State()
    standingback = State()

    goforward = standingforward.to(forward) | standingback.to(forward) | back.to(forward) | forward.to(forward)
    goback = standingforward.to(back) | standingback.to(back) | back.to(back) | forward.to(back)
    stop = back.to(standingback) | forward.to(standingforward) | standingforward.to(standingforward) | standingback.to(standingback)
    #stop = forward.to(standing) | back.to(standing)

    def __init__(self, obj):
        super().__init__(obj)
        self.last_direction = "right"

    def updateState(self):
        self.set_last_state(self.current_state.id)
        if self.hasVelocity() and self.isVelocityForward():
            if self.isVelocityRight():
                self.last_direction = "right"
            else:
                self.last_direction = "left"
            self.goforward()
        elif self.hasVelocity() and not self.isVelocityForward():
            if self.isVelocityRight():
                self.last_direction = "right"
            else:
                self.last_direction = "left"
            self.goback()
        elif self.noVelocity():
            self.stop()
        #elif self.noVelocity() and self.current_state != self.standing:
            #self.stop()

    def set_last_state(self, state):
        self.last_state = state

    def get_last_state(self):
        return self.last_state

    def hasVelocity(self):
        return magnitude(self.obj.velocity) > EPSILON

    def noVelocity(self):
        return not self.hasVelocity()

    def isVelocityForward(self):
        return self.obj.velocity[1] > 0
    
    def isVelocityRight(self):
        return self.obj.velocity[0] < 0

    def updateMovement(self, seconds):
        self.updateAnimation()
        if self.current_state == self.forward or self.current_state == self.back:
            self.obj.position += (self.obj.velocity * seconds).astype(int)


    def updateAnimation(self):
        state = self.current_state.id
        if state in ["forward", "back"]:
            if self.isVelocityForward():
                row = self.obj.rowList["forward"]
            else:
                row = self.obj.rowList["back"]
            self.obj.row = row
            self.obj.nFrames = self.obj.nFramesList[state]
            self.obj.framesPerSecond = self.obj.framesPerSecondList[state]
        if not self.isVelocityRight():
            self.flip = True
        else:
            self.flip = False
        if self.noVelocity:
            if self.last_direction == "right":
                self.flip = True
            else:
                self.flip = False
        self.obj.image = SpriteManager.getInstance().getSprite(self.obj.imageName,
                                                               (self.obj.frame, self.obj.row), self.obj.scale, self.flip)
        


class CustomerWalkingFSM(AnimateFSM):
    """Two-state FSM for walking / stopping in
       a top-down environment."""
       
    moving = State(initial=True)
    standing = State()
    
    move = standing.to(moving) | moving.to(moving)
    stop = moving.to(standing)
    
    def updateState(self):
        if self.hasVelocity() and self.current_state != self.moving:
            self.move()
        elif not self.hasVelocity() and self.current_state != self.standing:
            self.stop()
    
    def hasVelocity(self):
        return magnitude(self.obj.velocity) > EPSILON
    
    def noVelocity(self):
        return not self.hasVelocity()
    
    def updateMovement(self, seconds):
        if self.current_state == self.moving:
            self.updateAnimation(seconds)

    def updateAnimation(self, seconds):
        state = self.current_state.id
        self.obj.row = self.obj.rowList[state]
        self.obj.nFrames = self.obj.nFramesList[state]
        self.obj.framesPerSecond = self.obj.framesPerSecondList[state]
        self.obj.image = SpriteManager.getInstance().getSprite(
            self.obj.imageName,
            (self.obj.frame, self.obj.row),
            self.obj.scale,
            False  # Assuming flip is always False for customers
        )
