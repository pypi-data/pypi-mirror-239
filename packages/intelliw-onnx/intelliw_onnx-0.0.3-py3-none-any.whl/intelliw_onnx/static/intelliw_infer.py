import onnxruntime


class Algorithm:
    """
    算法类， 导入的算法必须定义class Algorithm， 并放入 algorithm.py 文件中
    """

    def __init__(self, parameters):
        """
        初始化， parameters 为 dict格式的参数信息， 比如
        {
            "params1": "value1",
            "params1", 2
        }
        """
        self.model = None
        self.parameters = parameters
        self.logger = self.parameters['framework_log']  # 日志

    def load(self, path):
        """
        加载模型
            不需要调用，只需要在这里实现加载模型的方法，并赋值给一个属性就可以，例如：
            self.model = xxxx.load(path)
            上线流程：算法框架会将模型文件放在model/下，然后进行函数的执行
            本地流程：可以通过model.yaml中location字段进行配置，然后会传入path参数
            Args:
                path : 模型文件路径，根据 model.yaml 文件中的 location 字段指定
            Returns:
                无
        """
        model_path = path
        self.model = onnxruntime.InferenceSession(model_path)

    def infer(self, infer_data):
        """
        推理
            推理服务Args:
                infer_data : 推理请求数据, json输入的参数, 类型可以为列表/字符串/字典

                如果使用特征工程, infer_data格式有硬性要求:
                {
                    "data": 任意格式，如果配置特征工程，此数据为处理后的数据 # 推理数据
                    "original_data":  原始输入的data ，防止数据在通过特征处理后丢失原先的数据
                }

                self.request dict[str, object]: 请求体
                    |- self.request.header  object: 请求头
                    |- self.request.files    ImmutableMultiDict[str, FileStorage]: 文件列表, 可以参照flask的文件读取
                    |- self.request.query   Dict[str]str: url参数
                    |- self.request.form    Dict[str]list: form表单参数
                    |- self.request.json    object: json参数
                    |- self.request.body    bytes: raw request data
                    批处理专有参数
                    |- self.request.batch_params List[Dict] 批处理输入参数,为请求中的json数据,用作任务间参数传递,请直接修改参数,不要deepcopy

            批处理服务Args:
                infer_data : 批处理输入数据
                            [{
                                "meta": [   // 表头
                                    {"code": "column_a"},
                                    {"code": "column_b"}
                                ],
                                "result": [ // 表体
                                    ["line_1_column_1", "line_1_column_2"],
                                    ["line_2_column_1", "line_2_column_2"]
                                ]
                            }]
                self.request dict[str, object]: 请求体
                    |- self.request.batch_params List[Dict]  批处理接口(/batch-predict)输入参数,为请求中的json数据,用作任务间参数传递,请直接修改参数,不要deepcopy

            Returns:
                推理结果, json
        """
        input_data = infer_data
        self.model.run(["output"], {"input": input_data})

        