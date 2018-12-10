from psychopy import visual
import numpy as np


class Dot():
    def __init__(self, window, radius, lineWidth, pos, velocity, acceleration):
        self.circle = visual.Circle(
            win=window,
            radius=radius,
            edges=32,
            pos=np.array(pos),
            lineColor='black',
            units='deg'
        )
        self.circle.lineWidth = lineWidth

        self.velocity       = np.array(velocity)
        self.acceleration   = np.array(acceleration)

    def update(self, dt=0):
        # 加速度の概念を導入するかどうか
        # 導入するならdtに経過時間を入れる
        print(self.circle.pos)
        print(self.velocity)
        print(self.acceleration)
        self.circle.pos += self.velocity + dt*self.acceleration
        self.draw()

    def draw(self):
        self.circle.draw()

if __name__ == '__main__':
    print("This file is just a class definition.")
    exit()