import math
from collections import namedtuple
from copy import copy
import random
from unittest import TestCase

import modules.scripts as scripts
import gradio as gr

from modules import images
from modules.processing import process_images, Processed
from modules.shared import opts, cmd_opts, state
import modules.sd_samplers

def convert_prompt(input):
    if ("{" not in input) and ("[" not in input): 
        return input

    tmp_prompt = repr(input)
    converted_prompt = ""

    tmp_prompt.replace('(','\(')
    tmp_prompt.replace(')','\)')
    tmp_prompt += ' '

    curly_iteration_count = tmp_prompt.count('{')
    square_iteration_count = tmp_prompt.count('[')

    try:
        for _ in range(curly_iteration_count):
            left_stack = []
            right_stack = []
            count = 0

            for i, ch in enumerate(tmp_prompt):
                if ch == '{':
                    left_stack.append(i)
                elif ch == '}':
                    count += 1
                    right_stack.append(i)
                else:
                    if count == 0:
                        pass
                    else:
                        converted_prompt = tmp_prompt[0:right_stack[0]] + ':{})'.format(round(1.05**count,6)) + tmp_prompt[right_stack[-1] + 1:]
                        converted_prompt = converted_prompt[0:left_stack[-count]] + '(' + converted_prompt[left_stack[-1] + 1:]
                        tmp_prompt = converted_prompt
                        break
        
        for _ in range(square_iteration_count):
            left_stack = []
            right_stack = []
            count = 0

            for i, ch in enumerate(tmp_prompt):
                if ch == '[':
                    left_stack.append(i)
                elif ch == ']':
                    count += 1
                    right_stack.append(i)
                else:
                    if count == 0:
                        pass
                    else:
                        converted_prompt = tmp_prompt[0:right_stack[0]] + ':{})'.format(round(0.952**count,6)) + tmp_prompt[right_stack[-1] + 1:]
                        converted_prompt = converted_prompt[0:left_stack[-count]] + '(' + converted_prompt[left_stack[-1] + 1:]
                        tmp_prompt = converted_prompt
                        break
    

        return eval(converted_prompt)

    except:
        return "SyntaxError:probably, your '{' and '}', or '[' and ']' are not same number"



class Script(scripts.Script):

    def title(self):
        return "nai2SD Prompt Converter"

    def ui(self, is_img2img):
        with gr.Column(scale=1):
            prompt_txt = gr.TextArea(label="Prompts")
            converter_button = gr.Button('convert')
            converted_prompt_txt = gr.TextArea(label="Converted Prompts")
            converter_button.click(
                fn=lambda x: convert_prompt(x),
                _js="nai prompt converted to sd prompt",
                inputs=[prompt_txt],
                outputs=[converted_prompt_txt],
            )

        return [prompt_txt,converter_button,converted_prompt_txt]

    def run(self, p, prompt_txt,converter_button,converted_prompt_txt):

        original_prompt = p.prompt[0] if type(p.prompt) == list else p.prompt
        
        p.prompt = original_prompt
        p.seed = p.seed
        p.prompt_for_display = original_prompt
        processed = process_images(p)

        return processed