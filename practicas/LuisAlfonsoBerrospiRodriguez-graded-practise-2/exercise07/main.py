import matplotlib.pyplot as plt

def are_intersecting(segments):
    events = []
    for segment in segments:
        events.append((segment[0], 'start', segment))
        events.append((segment[1], 'end', segment))
    
    events.sort()
           

    active_segments = set()
    for event in events:
        point, event_type, segment = event
        for s in segments:
                    plt.plot([s[0][0], s[1][0]], [s[0][1], s[1][1]], 'r-')
        
        if event_type == 'start':
            
            for active_segment in active_segments:
                if intersect(segment, active_segment):
                    return True
            active_segments.add(segment)
        else:
            active_segments.remove(segment)
    
    return False

def intersect(segment1, segment2):
    x1, y1 = segment1[0]
    x2, y2 = segment1[1]
    x3, y3 = segment2[0]
    x4, y4 = segment2[1]
    
    def ccw(a, b, c):
        return (c[1]-a[1]) * (b[0]-a[0]) > (b[1]-a[1]) * (c[0]-a[0])

    return ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and ccw((x1, y1), (x2, y2), (x3, y3)) != ccw((x1, y1), (x2, y2), (x4, y4))

# Example usage:
segments = [((1, 1), (4, 4)), ((2, 2), (5, 5)), ((3, 1), (5, 3)), ((1, 3), (4, 1))]
print('Expected:', True)
print(f'Got: {are_intersecting(segments)}')
# Example usage:
segments = [((1, 1), (1.5, 1.5)), ((2, 2), (2.5, 3)), ((4, 4.2), (4, 4.9)), ((1, 3), (2, 1.5))]
print('Expected:', False)
print(f'Got: {are_intersecting(segments)}')
