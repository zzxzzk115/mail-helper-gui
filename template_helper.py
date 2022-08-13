def get_config_dict(config_file_path: str) -> dict:
    with open(config_file_path) as f:
        config_lines = f.readlines()
        config_dict = {}
        for line in config_lines:
            clean_line = line.strip('\n')
            splitted_line = clean_line.split(',')
            config_item_key = splitted_line[0]
            config_item_value = splitted_line[1]
            config_dict[config_item_key] = config_item_value
        return config_dict


def get_rendered_html(html : str, config_dict : dict) -> str:
    result_html = html
    for key in config_dict:
        result_html = result_html.replace('{{!' + key + '}}', config_dict[key])
    return result_html


def test_template():
    html = open('test/template/example.html', 'r').read()
    config_dict = get_config_dict('test/template/example_config.txt')
    rendered_html = get_rendered_html(html, config_dict)
    print('Rendered Template HTML:\n')
    print(rendered_html)
    return rendered_html