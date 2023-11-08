
def update_config_file(filename):
    content = ''
    service_id = 'test_s_id2'
    service_group_id = 'test_sg_id2'
    with open(filename, 'r') as infile:
        sgi_found = False
        si_found = False
        for line in infile:
            if line.startswith('service_id'):
                content += f'service_id: {service_id}\n'
                si_found = True
            elif line.startswith('service_group_id'):
                content += f'service_group_id: {service_group_id}\n'
                sgi_found = True
            else:
                content += line
        if not sgi_found:
            content += f'service_group_id: {service_group_id}\n'
        if not si_found:
            content += f'service_id: {service_id}\n'
    with open(filename, 'w') as outfile:
        outfile.write(content)
    return f'成功创建服务{service_id}，服务ID已经写入文件{filename}。如果需要创建新版本，需要新建一个配置文件，切勿重用文件{filename}，否则会丢失本次新建的服务配置。'
    

if __name__ == '__main__':
    print(update_config_file('/root/.tikit/create_new_version.yaml'))
    
