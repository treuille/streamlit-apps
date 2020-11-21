import streamlit as st

"# Test ClassA"

a_global = 0

class ClassA:
    def __init__(self, a_value: int):
        self.a_value = a_value

    @st.cache(suppress_st_warning=True)
    def func(self):
        global a_global
        st.warning("Calling `st.cache()` "
            f"with `a_global={a_global}` and "
            f"with `self.a_value={self.a_value}`")
        a_global += 1 
        return (a_global, self.a_value)

"## First go"
obj_a = ClassA(42)
obj_a.a_value += 1
st.write(obj_a.func())
st.write(obj_a.func())
st.write(obj_a.func())

"## Second go"
obj_a.a_value += 1
st.write(obj_a.func())
st.write(obj_a.func())
st.write(obj_a.func())

"# Test ClassB"
    
class ClassB:
    def __init__(self, a_value: int):
        self.a_value = a_value
        self.a_local = 0 

    @st.cache(suppress_st_warning=True)
    def func(self):
        st.warning("Calling `st.cache()` "
            f"with `a_local={self.a_local}` and "
            f"with `self.a_value={self.a_value}`")
        self.a_local += 1 
        return (self.a_local, self.a_value)
    
"## First go"
obj_b = ClassB(42)
obj_b.a_value += 1
st.write(obj_b.func())
st.write(obj_b.func())
st.write(obj_b.func())

## Second go"
obj_b.a_value += 1
st.write(obj_b.func())
st.write(obj_b.func())
st.write(obj_b.func())
