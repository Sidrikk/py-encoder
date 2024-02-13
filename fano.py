class ShannonFanoNode:
    def __init__(self, symbol, probability):
        self.symbol = symbol
        self.probability = probability
        self.code = ""

def shannon_fano_coding(nodes):
    if len(nodes) == 1:
        return

    total_probability = sum(node.probability for node in nodes)
    cumulative_probability = 0
    half_probability = total_probability / 2

    for i, node in enumerate(nodes):
        cumulative_probability += node.probability
        if cumulative_probability >= half_probability:
            split_index = i
            break

    for i, node in enumerate(nodes):
        if i <= split_index:
            node.code += '0'
        else:
            node.code += '1'

    shannon_fano_coding(nodes[:split_index + 1])
    shannon_fano_coding(nodes[split_index + 1:])

def encode_shannon_fano(input_string):
    # Calculate probabilities of each symbol in the input string
    symbol_probabilities = {symbol: input_string.count(symbol) / len(input_string) for symbol in set(input_string)}

    # Create Shannon-Fano nodes for each symbol and probability
    nodes = [ShannonFanoNode(symbol, probability) for symbol, probability in symbol_probabilities.items()]

    # Sort nodes by probability in descending order
    nodes.sort(key=lambda x: x.probability, reverse=True)

    # Perform Shannon-Fano coding
    shannon_fano_coding(nodes)

    # Create a dictionary to store the code for each symbol
    code_dict = {node.symbol: node.code for node in nodes}

    # Encode the input string using the generated codes
    encoded_string = ''.join(code_dict[symbol] for symbol in input_string)

    return encoded_string, code_dict

# Пример использовани
