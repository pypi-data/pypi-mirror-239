# Automatic Brain Extraction Tools
```shell
Copyright Jiameng Liu, IDEA Lab, School of Biomedical Engineering, ShanghaiTech University.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

Repo for Automatic Brain Extraction Tools (AutoBET)
Contact: JiamengLiu.PRC@gmail.com
```

## Install
`pip install AutoBET`

### GPU accerate
Currently, our brain extraction tools works on GPU with at least 14G GPU memories. We are working on reduce the GPU capacity and will release it in the next version.

Due to the size limitation of PYPI we cannot include our model with the released AutoBET, please feel free to contact us to obtain our pretrained model (JiamengLiu.PRC@gmail.com)

## Usase

```python
from AutoBET.BET import Auto_BET, _model_init

source_img_path = '/path/to/your/T1/data'
target_img_path = '/path/to/your/skull/stripped/data'
target_seg_path = '/path/to/your/brain/mask'

model_path = '/path/to/pretrained/model'

model = _model_init(model_path)
Auto_BET(source_img_path, target_img_path, target_seg_path, model)
```