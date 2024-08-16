GEN_COUNT = 1000


def gen_test_code(unique_name: str) -> str:
    # This helps avoid identical code-gen which could skew results.
    rand_num = int(hash(unique_name)) % 100_000

    return f"""let mut vec_{unique_name} = vec![1, 2, {rand_num}];
vec_{unique_name}.push(3);
assert_eq!(vec_{unique_name}, [1, 2, {rand_num}, 3]);"""


def gen_fn_with_doc_test(unique_name: str) -> str:
    code = "\n".join([f"/// {line}" for line in gen_test_code(unique_name).split("\n")])

    return f"""/// This is a demo function, that contains a doc example.
///
/// # Example
///
/// ```
{code}
/// ```
pub fn {unique_name}() {{}}

"""


def gen_doc_test_file(gen_count) -> str:
    result = ""

    for i in range(gen_count):
        result += gen_fn_with_doc_test(f"example_fn_{i}")

    return result


def gen_it_test(unique_name: str) -> str:
    code = gen_test_code(unique_name)

    return f"""#[test]
fn {unique_name}() {{
    {code}
}}

"""


def gen_it_test_file(gen_count) -> str:
    result = ""

    for i in range(gen_count):
        result += gen_it_test(f"example_fn_{i}")

    return result


if __name__ == "__main__":
    print(gen_doc_test_file(GEN_COUNT))
    # print(gen_it_test_file(GEN_COUNT))
