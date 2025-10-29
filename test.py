#!/usr/bin/env python

import asyncio
import time
import uuid
import json


u = uuid.uuid4()

print(u)
print(f"type -> {type(u)}")
print(f"json -> {json.dumps({f"{u}": "hello"})}")
