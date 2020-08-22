#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, time, os, subprocess, time, shutil, json

testcases = [
    ('data/1.in', 'data/1.ans'),
    ('data/2.in', 'data/2.ans'),
    ('data/3.in', 'data/3.ans'),
    ('data/4.in', 'data/4.ans'),
    ('data/5.in', 'data/5.ans'),
    ('data/6.in', 'data/6.ans'),
    ('data/7.in', 'data/7.ans'),
    ('data/8.in', 'data/8.ans')
]

if __name__ == '__main__':

    if sys.version_info[0] != 3:
        print("Please use python3")
        exit(1)

    program_file = 'conflict.py'
    
    if not os.path.isfile(program_file):
        print('File {} not present!'.format(program_file))
        exit(1)

    success_count = 0

    for input, output in testcases:
        # remove the output file
        test_filename = 'grade.out'
        try:
            os.remove(test_filename)
        except:
            pass
        p = subprocess.Popen([sys.executable, program_file, input, test_filename], stdout=open(os.devnull,'w'), stderr=open(os.devnull,'w'))
        message = ''
        success = True
        start_time = time.time()
        while p.poll() is None:
            if time.time() - start_time > 1:
                p.terminate()
                message = 'Time limit exceeded'
                success = False
        else:
            if not os.path.isfile(test_filename):
                message = 'No output file found'
                success = False
            else:
                std = [line.strip() for line in open(output, 'r', encoding='utf-8').readlines() if line.strip()]
                ans = [line.strip() for line in open(test_filename, 'r', encoding='utf-8').readlines() if line.strip()]
                if len(std) != len(ans):
                    message = 'Line count mismatch'
                    success = False
                else:
                    for i in range(len(std)):
                        if std[i] != ans[i]:
                            message = 'Line {} mismatch: should be \'{}\', get \'{}\''.format(i, std[i], ans[i])
                            success = False
                            break
        if success:
            success_count += 1
            if os.isatty(1):
                print('Testcase {}: PASS'.format(input))
        else:
            if os.isatty(1):
                print('Testcase {}: {}'.format(input, message))
        
        
    grade = int(100.0 * success_count / len(testcases))
    
    if os.isatty(1):
        print('Total Points: {}/100'.format(grade))
    else:
        print(json.dumps({'grade': grade}))

