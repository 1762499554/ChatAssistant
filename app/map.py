from utils.logger import setup_logger


class Map:
    def __init__(self, city):
        self.logger = setup_logger()
        self.city = city

    def showmap(self):
        if self.city:
            map_url = f"https://picsum.photos/800/400?random={hash(self.city)}"

            map_info = f"""
                    ### {self.city} 地图 🗺️
                    ![{self.city}地图]({map_url})

                    点击下方链接在新窗口查看详细地图：
                    [百度地图 - {self.city}](https://map.baidu.com/search/{self.city})
                    """
            self.logger.info(f"地图显示: {self.city}")
        else:
            map_info = "请指定城市名称"
            self.logger.warning("地图显示缺少城市参数")

        return map_info


if __name__ == '__main__':
    map = Map('北京')
    map.showmap()