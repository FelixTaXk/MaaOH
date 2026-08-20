# agent/my_action.py  
import json  
  
from maa.agent.agent_server import AgentServer  
from maa.custom_action import CustomAction  
from maa.context import Context  
  
  
@AgentServer.custom_action("SetTargetByOcrCount")  
class SetTargetByOcrCount(CustomAction):  
  
    def run(  
        self,  
        context: Context,  
        argv: CustomAction.RunArg,  
    ) -> bool:  
  
        # node1 通过 custom_action_param 传入 target_node（即 node2 的节点名）  
        # custom_action_param 在 pipeline 中是字符串，需要自行解析  
        param = json.loads(argv.custom_action_param) if argv.custom_action_param else {}  
        target_node = param.get("target_node", "node2")  
  
        # argv.reco_detail 就是触发本 action 的节点（node1）的识别结果，  
        # 不需要再单独 run_recognition  
        count = 0  
        if argv.reco_detail is not None:  
            count = len(argv.reco_detail.filterd_results)  
  
        count = max(0, min(count, 2))  
  
        target_map = {  
            0: [0, 0, 0, 0],  
            1: [1, 1, 1, 1],  
            2: [2, 2, 2, 2],  
        }  
  
        # 动态覆写 node2 的 target  
        context.override_pipeline({  
            target_node: {  
                "target": target_map[count],  
            }  
        })  
  
        return True