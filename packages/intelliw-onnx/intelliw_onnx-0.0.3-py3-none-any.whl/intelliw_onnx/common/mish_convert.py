import onnx
import argparse
from intelliw_onnx.utils.logger import get_logger

logger = get_logger("CONVERT")


def merge_mish(model):
    dict_sp = {}
    dict_tanh = {}
    dict_mul = {}

    got_mish = False

    search = True

    while search:
        search = False
        for node_id, node in enumerate(model.graph.node):

            if node.op_type == 'Softplus':
                dict_sp['input'] = node.input
                dict_sp['output'] = node.output
                dict_sp['id'] = node_id

            if node.op_type == 'Tanh':
                if dict_sp and node.input == dict_sp['output']:
                    dict_tanh['input'] = node.input
                    dict_tanh['output'] = node.output
                    dict_tanh['id'] = node_id
                    logger.debug('got first pair: {} {}'.format(dict_tanh['input'], dict_tanh['output']))
                else:
                    logger.debug('clear Softplus, dict_sp: {}'.format(dict_sp))
                    dict_sp = {}

            if node.op_type == 'Mul':
                if dict_sp and dict_tanh and node.input[1] == dict_tanh['output'][0] and node.input[0] == \
                        dict_sp['input'][0]:
                    dict_mul['input'] = node.input
                    dict_mul['output'] = node.output
                    dict_mul['id'] = node_id

                    logger.debug('got second pair: {} {}'.format(dict_mul['input'], dict_mul['output']))

                    got_mish = True

                    old_node = model.graph.node[dict_sp['id']]
                    model.graph.node.remove(old_node)

                    mish_node = onnx.helper.make_node(
                        name='',
                        op_type='Mish',
                        inputs=dict_sp['input'],
                        outputs=dict_mul['output'],
                        domain='com.metax-tech'
                    )

                    model.graph.node.insert(dict_sp['id'], mish_node)

                    # for node in mish_next_list:
                    # next_node = model.graph.node[node['id']]
                    # next_node.input[0] = dict_sp['output'][0]

                    old_node = model.graph.node[dict_mul['id']]
                    model.graph.node.remove(old_node)

                    old_node = model.graph.node[dict_tanh['id']]
                    model.graph.node.remove(old_node)

                    dict_sp = {}
                    dict_tanh = {}
                    dict_mul = {}

                    search = True
                    break
                else:
                    logger.debug('clear Softplus and Tanh')
                    logger.debug('dict_sp: {}'.format(dict_sp))
                    logger.debug('dict_tanh: {}'.format(dict_tanh))
                    dict_sp = {}
                    dict_tanh = {}

    if got_mish:
        op_set = model.opset_import.add()
        op_set.domain = 'com.metax-tech'
        op_set.version = 1

    return model


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Softplus+Tanh+Mul to Mish')
    parser.add_argument('--onnx_file', type=str, default='', help='source onnx model')
    args = parser.parse_args()
    merge_mish(args.onnx_file)
