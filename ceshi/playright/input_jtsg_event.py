from make_data import BaseDatas
from add_event_phone import AddEvent
from login_api import get_token_by_phone
from get_road_info import get_road_info


class InputJtsgEvent:
    def __init__(self):
        self.base_data = BaseDatas()
        self.token = get_token_by_phone()
        self.add_event = AddEvent(self.token)
        self.road_info = get_road_info(self.token)

    def input_jtsg_event(self):
        err_road = []
        err_road_dic = {}
        num = 0
        for road_info in self.road_info:
            expresswayId = road_info['roadId']  # 道路编号
            startPileNo = BaseDatas().get_road_no(road_info['roadNameRange'])  # 道路桩号
            roadCode = road_info['roadCode']  # 道路code
            for direction_ in road_info['direction']:
                eventDescrible = f'{road_info['roadName']}{direction_['direction']},车辆发生撞障碍物事故,占用超车道,行车道正常通行,请过往车辆减速慢行。'
                direction = direction_['direction']  # 方向
                updown = direction_['updown']  # 上下行
                # 添加事件
                response = self.add_event.jtsg_road_event(expresswayId, startPileNo, eventDescrible, direction, updown, roadCode)
                print(f"第{num}条数据,{road_info['roadName']}{direction_['direction']}:", response)
                num += 1
                if 'status' in response.keys():
                    err_road_dic['roadName'] = road_info['roadName']
                    err_road_dic['direction'] = direction_['direction']
                    err_road_dic['updown'] = direction_['updown']
                    err_road_dic['response'] = response
                    err_road.append(err_road_dic)
        print(err_road)


if __name__ == '__main__':
    input_jtsg_event = InputJtsgEvent()
    input_jtsg_event.input_jtsg_event()
