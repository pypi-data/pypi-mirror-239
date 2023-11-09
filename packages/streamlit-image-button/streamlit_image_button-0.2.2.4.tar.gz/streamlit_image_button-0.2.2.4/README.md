# streamlit-custom-component

Streamlit component that allows you to add clickable buttons with .png or .jpg image replacing text.

## Installation instructions

```sh
pip install streamlit-image-button
```

## Usage instructions

```python
import streamlit as st

from st_image_button import st_image_button

st_image_button("Title", "icon.png", "20px", "outlined", onClick)
```