from pipeline.core.box_data import SpeechBubble



def overlap(speech_bubbles_data: list[SpeechBubble]) -> list[SpeechBubble]:
    result = overlapping_box(speech_bubbles_data)

    for box in result:
        intersection = intersection_box(box[0].position, box[1].position)
        print("INTERSECTION:", intersection)

        if intersection is None:
            continue

        # Ensure we never remove all clusters from a bubble due to overlap pruning
        for c in list(box[0].text_clusters or []):
            if is_text_cluster_inside_intersection(c.position, intersection):
                if box[0].text_clusters and len(box[0].text_clusters) > 1:
                    box[0].text_clusters.remove(c)

        for c in list(box[1].text_clusters or []):
            if is_text_cluster_inside_intersection(c.position, intersection):
                if box[1].text_clusters and len(box[1].text_clusters) > 1:
                    box[1].text_clusters.remove(c)

    return speech_bubbles_data


def rectangles_overlap(rect1: tuple[int, int, int, int], rect2: tuple[int, int, int, int]) -> bool:
    x1_min, y1_min, x1_max, y1_max = rect1
    x2_min, y2_min, x2_max, y2_max = rect2

    return not (x1_max < x2_min or x2_max < x1_min or y1_max < y2_min or y2_max < y1_min)


def overlapping_box(speech_bubbles_data: list[SpeechBubble]) -> list[tuple[int, int]]:
    overlaps = []
    n = len(speech_bubbles_data)
    
    for i in range(n):
        for j in range(i+1, n):
            if rectangles_overlap(speech_bubbles_data[i].position, speech_bubbles_data[j].position):
                overlaps.append((speech_bubbles_data[i], speech_bubbles_data[j]))

    return overlaps


def intersection_box(box1: tuple[int, int, int, int], box2: tuple[int, int, int, int]):
    Ax_min, Ay_min, Ax_max, Ay_max = box1
    Bx_min, By_min, Bx_max, By_max = box2

    Ix_min = max(Ax_min, Bx_min)
    Iy_min = max(Ay_min, By_min)
    Ix_max = min(Ax_max, Bx_max)
    Iy_max = min(Ay_max, By_max)

    if Ix_min < Ix_max and Iy_min < Iy_max:
        return (Ix_min, Iy_min, Ix_max, Iy_max)
    
    return None


def is_text_cluster_inside_intersection(TC_pos, Intersection_pos):
    p = 0.10
    TCx_min, TCy_min, TCx_max, TCy_max = TC_pos
    width = TCx_max - TCx_min
    height = TCy_max - TCy_min

    TCx_min_new = TCx_min + width * p
    TCx_max_new = TCx_max
    TCy_min_new = TCy_min + height * p
    TCy_max_new = TCy_max - height * p

    Ix_min, Iy_min, Ix_max, Iy_max = Intersection_pos

    return (Ix_min <= TCx_min_new <= Ix_max and
            Ix_min <= TCx_max_new <= Ix_max and
            Iy_min <= TCy_min_new <= Iy_max and
            Iy_min <= TCy_max_new <= Iy_max)
    