import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "st_image_button",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_image_button", path=build_dir)


def st_image_button(title, image, width, variant = "outlined", key = None):

    _ = _component_func(title = title, image = image, width = width, variant = variant, key = None)

if __name__ == "__main__":
    
    import streamlit as st

    st.subheader("Test 1")

    if st_image_button("Title", "icon.png", "20px", "outlined"):
        
        st.write("OK")
    st.markdown("---")
