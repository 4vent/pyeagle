import json
from datetime import datetime
from typing import Any

import pyeagle


def _testout(data: str | bytes | dict[Any, Any] | pyeagle.types.APIResponce | list):
    filename = 'log/' + datetime.now().isoformat().replace(':', '-')
    if isinstance(data, dict) or isinstance(data, pyeagle.types.APIResponce):
        with open(filename + '.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False,
                      cls=pyeagle.EagleJSONEncoder)
    elif isinstance(data, list):
        with open(filename + '.json', 'w') as f:
            json.dump({'data': data}, f, indent=4, ensure_ascii=False,
                      cls=pyeagle.EagleJSONEncoder)
    else:
        try:
            data = json.loads(data)
            with open(filename + '.json', 'w') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except json.decoder.JSONDecodeError:
            with open(filename + '.txt', 'w') as f:
                f.write(data)  # type: ignore


api = pyeagle.EagleAPI()
api.utility.renameItem('LAK2MLKQTJNUV', 'renaaaaaaaaaaaameee!!!')