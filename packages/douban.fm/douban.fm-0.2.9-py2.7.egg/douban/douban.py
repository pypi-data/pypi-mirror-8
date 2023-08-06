#!/usr/bin/env python
#-*- encoding: UTF-8 -*-
"""
豆瓣FM主程序
"""
#---------------------------------import------------------------------------
import cli # UI
import douban_token # network
import getch # get char
import lrc2dic # lrc
import subprocess
from termcolor import colored
import threading
import string
import time
import os
import ConfigParser
import platform
try:
    import Foundation
    import objc
    import AppKit
except ImportError:
    pass
#---------------------------------------------------------------------------
class Win(cli.Cli):

    def __init__(self, douban):
        self.platform = platform.system()
        self.get_config()
        self.douban = douban
        if self.douban.pro == 0:
            PRO = ''
        else:
            PRO = colored(' PRO ', attrs = ['reverse'])
        self.TITLE += self.douban.user_name + ' ' + PRO + ' ' + ' >>\r'
        self.start = 0 # 歌曲播放
        self.q = 0 # 退出
        self.song_time = -1 # 歌曲剩余播放时间
        self.rate = ['★ '*i for i in range(1,6)] # 歌曲评分
        self.lrc_display = 0 # 是否显示歌词
        # 守护线程
        self.t1 = threading.Thread(target=self.protect)
        self.t2 = threading.Thread(target=self.display_time)
        self.t1.start()
        self.t2.start()
        super(Win, self).__init__(self.douban.lines)
        # 启动自动播放
        self.SUFFIX_SELECTED = '正在加载请稍后...'
        self.display()
        self.douban.set_channel(self.douban.channels[self.markline]['channel_id']) # 设置默认频率
        self.douban.get_playlist()
        self.play()
        self.start = 1
        self.run()

    # 获取config
    def get_config(self):
        config=ConfigParser.ConfigParser()
        with open(os.path.expanduser('~/.doubanfm_config'),'r') as cfgfile:
            config.readfp(cfgfile)
            self.UP = config.get('key','UP')
            self.DOWN = config.get('key','DOWN')
            self.TOP = config.get('key','TOP')
            self.BOTTOM = config.get('key','BOTTOM')
            self.OPENURL = config.get('key','OPENURL')
            self.RATE = config.get('key','RATE')
            self.NEXT = config.get('key','NEXT')
            self.BYE = config.get('key','BYE')
            self.QUIT = config.get('key','QUIT')

    # 显示时间,音量的线程
    def display_time(self):
        length = len(self.TITLE)
        while True:
            if self.q == 1:
                break
            if self.song_time >= 0 and self.douban.playingsong:
                minute = int(self.song_time) / 60
                sec = int(self.song_time) % 60
                show_time = string.zfill(str(minute), 2) + ':' + string.zfill(str(sec), 2)
                self.get_volume() # 获取音量
                self.TITLE = self.TITLE[:length - 1] + '  ' + self.douban.playingsong['kbps'] + 'kbps  ' + colored(show_time, 'cyan') + '  rate: ' + colored(self.rate[int(round(self.douban.playingsong['rating_avg'])) - 1], 'red') + '  vol: ' + self.volume.strip() + '%' + '\r'
                if not self.lrc_display:
                    self.display()
                self.song_time -= 1
            else:
                self.TITLE = self.TITLE[:length]
            time.sleep(1)

    # 获取音量
    def get_volume(self):
        if self.platform == 'Linux':
            volume = subprocess.check_output('amixer get Master | grep Mono: | cut -d " " -f 6', shell=True)
            volume = volume[1:-3]
        elif self.platform == 'Darwin':
            volume = subprocess.check_output('osascript -e "output volume of (get volume settings)"', shell=True)
        else:
            volume = ''
        self.volume = volume

    # 调整音量大小
    def change_volume(self, increment):
        if increment == 1:
            volume = int(self.volume) + 5
        else:
            volume = int(self.volume) - 5
        if self.platform == 'Linux':
            subprocess.Popen('amixer set Master ' + str(volume) + '% >/dev/null 2>&1', shell=True)
        elif self.platform == 'Darwin':
            subprocess.Popen('osascript -e "set volume output volume ' + str(volume) + '"', shell=True)
        else:
            pass

    # 守护线程,检查歌曲是否播放完毕
    def protect(self):
        while True:
            if self.q == 1:
                break
            if self.start:
                self.p.poll()
                if self.p.returncode == 0:
                    self.song_time = -1
                    self.douban.end_music()
                    self.play()
            time.sleep(1)

    # 播放歌曲
    def play(self):
        self.douban.get_song()
        song = self.douban.playingsong
        self.song_time = song['length']
        # 是否是红心歌曲
        if song['like'] == 1:
            love = self.love
        else:
            love = ''
        self.SUFFIX_SELECTED = (love + colored(song['title'], 'green') + ' • ' + colored(song['albumtitle'], 'yellow') + ' • ' + colored(song['artist'], 'white') + ' ' + song['public_time']).replace('\\', '')

        self.p = subprocess.Popen('mplayer ' + song['url'] + ' -slave  >/dev/null 2>&1', shell=True, stdin=subprocess.PIPE) # subprocess.PIPE防止继承父进程
        self.display()
        self.notifySend()

    # 结束mplayer
    def kill_mplayer(self):
        if subprocess.check_output('ps -a | grep mplayer', shell=True):
            subprocess.Popen('killall -9 mplayer >/dev/null 2>&1', shell=True)

    # 发送桌面通知
    def notifySend(self, title=None, content=None, path=None):
        if not title and not content:
            title = self.douban.playingsong['title']
        elif not title:
            title = self.douban.playingsong['title'] + ' - ' + self.douban.playingsong['artist']
        if not path:
            path = self.douban.get_pic() # 获取封面
        if not content:
            content = self.douban.playingsong['artist']

        if self.platform == 'Linux':
            self.send_Linux_notify(title, content, path)
        elif self.platform == 'Darwin':
            self.send_OS_X_notify(title, content, path)

    def send_Linux_notify(self, title, content, img_path):
        subprocess.call([ 'notify-send', '-i', img_path, title, content])

    def send_OS_X_notify(self, title, content, img_path):
        NSUserNotification = objc.lookUpClass('NSUserNotification')
        NSUserNotificationCenter = objc.lookUpClass('NSUserNotificationCenter')
        NSImage = objc.lookUpClass('NSImage')
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(title.decode('utf-8'))
        notification.setSubtitle_('')
        notification.setInformativeText_(content.decode('utf-8'))
        notification.setUserInfo_({})
        image = NSImage.alloc().initWithContentsOfFile_(img_path)
        notification.setContentImage_(image)
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
        notification.setDeliveryDate_(Foundation.NSDate.dateWithTimeInterval_sinceDate_(0, Foundation.NSDate.date()))
        NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)


    def run(self):
        while True:
            self.display()
            i = getch._Getch()
            c = i()
            if c == self.UP:
                self.updown(-1)
            elif c == self.DOWN:
                self.updown(1)
            elif c == self.TOP: # g键返回顶部
                self.markline = 0
                self.topline = 0
            elif c == self.BOTTOM: # G键返回底部
                self.markline = self.screenline
                self.topline = len(self.lines) - self.screenline - 1
            elif c == ' ': # 空格选择频道,播放歌曲
                if self.markline + self.topline != self.displayline:
                    if self.douban.playingsong:
                        self.douban.playingsong = {}
                        self.kill_mplayer()
                    self.displaysong()
                    self.SUFFIX_SELECTED = '正在加载请稍后...'
                    self.display()
                    self.douban.set_channel(self.douban.channels[self.markline + self.topline]['channel_id'])
                    self.douban.get_playlist()
                    self.play()
                    self.start = 1
            elif c == self.OPENURL: # l打开当前播放歌曲豆瓣页
                import webbrowser
                webbrowser.open("http://music.douban.com" + self.douban.playingsong['album'].replace('\/', '/'))
                self.display()
            elif c == self.RATE: # r标记红心/取消标记
                if self.douban.playingsong:
                    if not self.douban.playingsong['like']:
                        self.SUFFIX_SELECTED = self.love + self.SUFFIX_SELECTED
                        self.display()
                        self.douban.rate_music()
                        self.douban.playingsong['like'] = 1
                        self.notifySend(content='标记红心')
                    else:
                        self.SUFFIX_SELECTED = self.SUFFIX_SELECTED[len(self.love):]
                        self.display()
                        self.douban.unrate_music()
                        self.douban.playingsong['like'] = 0
                        self.notifySend(content='取消标记红心')
            elif c == self.NEXT: # n下一首
                if self.douban.playingsong:
                    self.kill_mplayer()
                    self.SUFFIX_SELECTED = '正在加载请稍后...'
                    self.display()
                    self.douban.skip_song()
                    self.douban.playingsong = {}
                    self.play()
            elif c == self.BYE: # b不再播放
                if self.douban.playingsong:
                    self.SUFFIX_SELECTED = '不再播放,切换下一首...'
                    self.display()
                    self.kill_mplayer()
                    self.douban.bye()
                    self.play()
            elif c == self.QUIT:
                self.q = 1
                if self.start:
                    self.kill_mplayer()
                subprocess.call('echo -e "\033[?25h";clear', shell=True)
                exit()
            elif c == '=':
                self.change_volume(1)
            elif c == '-':
                self.change_volume(-1)
            elif c == 'o':
                self.lrc_display = 1
                lrc_dic = self.douban.get_lrc()
                if lrc_dic:
                    lrc_cli = Lrc(lrc_dic, int(self.douban.playingsong['length']) , self.song_time, self.screenline)
                self.lrc_display = 0

class Lrc(cli.Cli):
    def __init__(self, lrc_dic, length, song_time,screenline):
        self.lrc_dic = lrc_dic
        self.length = length
        self.song_time = length - song_time
        self.sort_lrc_dic = sorted(lrc_dic.iteritems(), key=lambda x : x[0])
        lrc_lines = [line[1] for line in self.sort_lrc_dic]
        # super(Lrc, self).__init__(lrc_lines)
        self.lines = lrc_lines
        self.screenline = screenline
        subprocess.call('echo  "\033[?25l"', shell=True)
        self.markline = self.locate_line()
        # print self.markline
        self.topline = self.markline
        # print self.topline
        self.q = 0
        t = threading.Thread(target=self.display_line)
        t.start()
        self.run()

    # 根据song_time定位self.markline
    def locate_line(self):
        tmp = range(self.song_time)
        for i in tmp[::-1]:
            if self.lrc_dic.has_key(i):
                return self.lines.index(self.lrc_dic[i])
        return 0

    def display_line(self):
        while True:
            if self.q:
                break
            if self.song_time < self.length:
                self.song_time += 1
                if self.lrc_dic.has_key(self.song_time):
                    self.updown(1)
                self.display()
                time.sleep(1)
            else:
                break

    def display(self):
        subprocess.call('clear', shell=True)
        print
        top = self.topline
        bottom = self.topline + self.screenline + 1
        for index,i in enumerate(self.lines[top:bottom]):
            if index == self.markline:
                i = colored(i, 'blue')
            print i + '\r'

    def run(self):
        while True:
            self.display()
            i = getch._Getch()
            c = i()
            if c == 'q':
                self.q = 1
                break

def main():
    douban = douban_token.Doubanfm()
    w = Win(douban)

if __name__ == '__main__':
    main()
############################################################################
