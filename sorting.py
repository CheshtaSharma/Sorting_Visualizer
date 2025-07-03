def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(n - i - 1):
            yield data, {j: '#FFD700', j + 1: '#FFD700'}  # Comparing
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
        yield data, {n - i - 1: '#90EE90'}  # Sorted element
    yield data, {i: '#90EE90' for i in range(len(data))}


def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and data[j] > key:
            yield data, {j: '#FFD700', j + 1: '#FFD700'}
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key
    yield data, {i: '#90EE90' for i in range(len(data))}


def merge_sort(data, start, end):
    if start >= end:
        return
    mid = (start + end) // 2
    yield from merge_sort(data, start, mid)
    yield from merge_sort(data, mid + 1, end)
    yield from merge(data, start, mid, end)
    yield data, {}


def merge(data, start, mid, end):
    merged = []
    left = start
    right = mid + 1

    while left <= mid and right <= end:
        yield data, {left: '#FFD700', right: '#FFD700'}
        if data[left] < data[right]:
            merged.append(data[left])
            left += 1
        else:
            merged.append(data[right])
            right += 1

    while left <= mid:
        merged.append(data[left])
        left += 1
    while right <= end:
        merged.append(data[right])
        right += 1

    for i, val in enumerate(merged):
        data[start + i] = val
        yield data, {start + i: '#FFD700'}  # Optional: yellow on merge

    yield data, {i: '#90EE90' for i in range(len(data))}


def quick_sort(data, low, high):
    if low < high:
        pivot_index, updates = partition(data, low, high)
        for step in updates:
            yield step
        yield from quick_sort(data, low, pivot_index - 1)
        yield from quick_sort(data, pivot_index + 1, high)
    else:
        yield data, {}


def partition(data, low, high):
    pivot = data[high]
    i = low - 1
    updates = []

    for j in range(low, high):
        updates.append((data[:], {j: '#FFD700', high: '#FFD700'}))
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
        updates.append((data[:], {j: '#FFD700'}))  # Reset

    data[i + 1], data[high] = data[high], data[i + 1]
    updates.append((data[:], {i + 1: '#FFD700', high: '#FFD700'}))
    updates.append((data[:], {i + 1: '#90EE90'}))  # Sorted pivot

    return i + 1, updates


def selection_sort(data):
    n = len(data)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            yield data, {min_index: '#FFD700', j: '#FFD700'}
            if data[j] < data[min_index]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]
        yield data, {i: '#90EE90'}  # Sorted
    yield data, {i: '#90EE90' for i in range(len(data))}


def heap_sort(data):
    n = len(data)

    def heapify(n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and data[l] > data[largest]:
            largest = l
        if r < n and data[r] > data[largest]:
            largest = r

        yield data, {i: '#FFD700', largest: '#FFD700'}

        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            yield from heapify(n, largest)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)

    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        yield from heapify(i, 0)

    yield data, {i: '#90EE90' for i in range(len(data))}

