# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========== Copyright 2023 @ CAMEL-AI.org. All Rights Reserved. ===========

from pydantic import BaseModel

from camel.schemas import OpenAISchemaConverter
from camel.utils import get_pydantic_model


class Temperature(BaseModel):
    location: str
    date: str
    temperature: float


def get_temperature(location: str, date: str, temperature: float):
    print(f"Temperature in {location} on {date} is {temperature} degrees.")


def test_openai_converter_with_str_template():
    temperature_template = (
        '{"location": "Beijing", "date": "2023-09-01", "temperature": 30.0}'
    )
    target_format_from_str = get_pydantic_model(temperature_template)

    model = OpenAISchemaConverter(
        output_schema=target_format_from_str,
    )

    structured_output = model.convert(
        "Today is 2023-09-01, the temperature in Beijing is 30 degrees."
    )

    assert structured_output.model_dump() == {
        "location": "Beijing",
        "date": "2023-09-01",
        "temperature": 30.0,
    }


def test_openai_converter_with_function():
    target_format_from_function = get_pydantic_model(get_temperature)

    model = OpenAISchemaConverter(
        output_schema=target_format_from_function,
    )

    structured_output = model.convert(
        "Today is 2023-09-01, the temperature in Beijing is 30 degrees."
    )

    assert structured_output.model_dump() == {
        "location": "Beijing",
        "date": "2023-09-01",
        "temperature": 30.0,
    }


def test_openai_converter_with_model():
    target_format_from_model = Temperature

    model = OpenAISchemaConverter(
        output_schema=target_format_from_model,
    )

    structured_output = model.convert(
        "Today is 2023-09-01, the temperature in Beijing is 30 degrees."
    )

    assert structured_output.model_dump() == {
        "location": "Beijing",
        "date": "2023-09-01",
        "temperature": 30.0,
    }
