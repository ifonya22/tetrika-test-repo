def appearance(intervals: dict[str, list[int]]) -> int:
    def merge_intervals(times: list) -> list:
        if not times:
            return []

        intervals = list(zip(times[::2], times[1::2]))

        intervals.sort()

        merged = []
        for current in intervals:
            if not merged:
                merged.append(current)
            else:
                last = merged[-1]
                if current[0] <= last[1]:
                    new_start = last[0]
                    new_end = max(last[1], current[1])
                    merged[-1] = (new_start, new_end)
                else:
                    merged.append(current)

        return merged

    pupil = merge_intervals(intervals["pupil"])
    tutor = merge_intervals(intervals["tutor"])

    lesson = intervals["lesson"]

    total_time = 0
    i, j = 0, 0
    while True:
        if i >= len(pupil) or j >= len(tutor):
            break
        pupil_start = pupil[i][0]
        tutor_start = tutor[j][0]
        pupil_end = pupil[i][1]
        tutor_end = tutor[j][1]

        start = max(pupil_start, tutor_start)
        end = min(pupil_end, tutor_end)
        if start < end:
            overlap_start = max(start, lesson[0])
            overlap_end = min(end, lesson[1])
            if overlap_start < overlap_end:
                total_time += overlap_end - overlap_start
        if tutor_end > pupil_end:
            i += 1
        else:
            j += 1

    return total_time


tests = [
    {
        "intervals": {
            "lesson": [1594663200, 1594666800],
            "pupil": [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
            "tutor": [1594663290, 1594663430, 1594663443, 1594666473],
        },
        "answer": 3117,
    },
    {
        "intervals": {
            "lesson": [1594702800, 1594706400],
            "pupil": [
                1594702789,
                1594704500,
                1594702807,
                1594704542,
                1594704512,
                1594704513,
                1594704564,
                1594705150,
                1594704581,
                1594704582,
                1594704734,
                1594705009,
                1594705095,
                1594705096,
                1594705106,
                1594706480,
                1594705158,
                1594705773,
                1594705849,
                1594706480,
                1594706500,
                1594706875,
                1594706502,
                1594706503,
                1594706524,
                1594706524,
                1594706579,
                1594706641,
            ],
            "tutor": [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463],
        },
        "answer": 3577,
    },
    {
        "intervals": {
            "lesson": [1594692000, 1594695600],
            "pupil": [1594692033, 1594696347],
            "tutor": [1594692017, 1594692066, 1594692068, 1594696341],
        },
        "answer": 3565,
    },
]

if __name__ == "__main__":
    for i, test in enumerate(tests):
        test_answer = appearance(test["intervals"])
        assert test_answer == test["answer"], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
