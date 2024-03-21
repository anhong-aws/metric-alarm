# This is the generator function that simulates processing data.
def collect_data(data_set):
    for data in data_set:
        # Simulate data processing by adding 10 to each item.
        processed_data = data + 10
        yield processed_data

# This is the consumer function that uses the generator.
def run():
    results = []
    for data in collect_data([1, 2, 3, 4, 5]):
        # Handle each processed data by multiplying it by 2.
        print(data)
        results.append(data * 2)
    print(results)
    return results

# Test case to verify the functionality.
def test_run():
    assert run() == [22, 24, 26, 28, 30], "The run function did not produce the expected results."

# Running the test case.
test_run()
