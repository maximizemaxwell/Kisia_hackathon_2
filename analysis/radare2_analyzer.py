import r2pipe


def analyze_file(file_path):
    r2 = r2pipe.open(file_path)
    r2.cmd('aaa')
    info = r2.cmdj('iIj')
    functions = r2.cmdj('aflj')
    strings = r2.cmdj('izj')
    sections = r2.cmdj('iSj')
    r2.quit()

    analysis_result = {
        'info': info,
        'functions': functions,
        'strings': strings,
        'sections': sections
    }

    return analysis_result
