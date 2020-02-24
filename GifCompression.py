from pygifsicle import optimize,gifsicle
import imageio
import random
import math

class GifCompression:
    def __init__(self, URI, GAP=0.4):
        '''
        self.URI 	是指的文件路径
        self.GAP 	是指的抽离掉(0~1)部分,例如self.GAP=0.4意味着删除其中40%的帧
        self.IM  	是指的读出的图片
        self.FRAMES 是指GIF有多少帧
        self.DUR 	是指GIF每帧的时间间隔
        '''
        self.URI = URI
        self.GAP = GAP
        self.IM = imageio.get_reader(URI)
        self.FRAMES = len(self.IM)
        before_dur = self.IM.get_meta_data()['duration']
        processed_frames = int(self.FRAMES * (1 - self.GAP))
        dur = round((self.FRAMES * before_dur) / (processed_frames * 10)) * 10
        real_frames = round((self.FRAMES * before_dur) / float(dur))
        self.GAP = (self.FRAMES - real_frames) / self.FRAMES
        print("before GIF frames:", self.FRAMES, ",DUR:", before_dur)
        print("After dynamic adjustment:", real_frames, ",DUR:", dur)
        self.DUR = dur / 1000
        self.images = []

    def calculation_reservation(self):
        averg = self.FRAMES * self.GAP  # 计算平均值
        step = self.FRAMES / averg  	# 计算步进值
        imagesindex = [i for i in range(self.FRAMES)]
        count = self.FRAMES
        intcount = self.FRAMES
        for i in range(int(averg)):
            count -= step
            if random.randint(1, 2) != 1:
                intcount = int(count)
                imagesindex.pop(intcount)
            else:
                intcount = math.ceil(count)
                imagesindex.pop(intcount)
        return imagesindex

    def image_append(self):
        imagesindex = self.calculation_reservation()
        count = 0
        for frame in self.IM:
            if count in imagesindex:
                self.images.append(frame)
            count += 1

    def save_images(self, save_uri):
        self.image_append()
        imageio.mimsave(save_uri, self.images, 'GIF', duration=self.DUR)
        print("GIF export complete!")
        optimize(save_uri)
        print("GIF optimize complete!")
        gifsicle(sources=[save_uri],optimize=False,options=['-O3'])
        print("GIF deep optimize complete!")


gif = GifCompression("before.gif")
gif.save_images('after.gif')
