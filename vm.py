import matplotlib.pyplot as plt

def fifo(pages, frame_size):
    frame = []
    queue = []
    faults = 0
    hits = 0

    for page in pages:
        if page not in frame:
            faults += 1
            if len(frame) < frame_size:
                frame.append(page)
                queue.append(page)
            else:
                oldest = queue.pop(0)
                frame[frame.index(oldest)] = page
                queue.append(page)
        else:
            hits += 1
    return faults, hits

def lru(pages, frame_size):
    frame = []
    recent = []
    faults = 0
    hits = 0

    for page in pages:
        if page not in frame:
            faults += 1
            if len(frame) < frame_size:
                frame.append(page)
            else:
                lru_page = recent.pop(0)
                frame[frame.index(lru_page)] = page
        else:
            hits += 1
            recent.remove(page) if page in recent else None
        recent.append(page)
    return faults, hits

def optimal(pages, frame_size):
    frame = []
    faults = 0
    hits = 0

    for i, page in enumerate(pages):
        if page not in frame:
            faults += 1
            if len(frame) < frame_size:
                frame.append(page)
            else:
                future_uses = []
                for f_page in frame:
                    if f_page in pages[i+1:]:
                        future_uses.append(pages[i+1:].index(f_page))
                    else:
                        future_uses.append(float('inf'))
                index_to_replace = future_uses.index(max(future_uses))
                frame[index_to_replace] = page
        else:
            hits += 1
    return faults, hits

def plot_results(results):
    algorithms = list(results.keys())
    faults = [results[algo]['faults'] for algo in algorithms]
    hits = [results[algo]['hits'] for algo in algorithms]

    plt.figure(figsize=(10,5))
    plt.bar(algorithms, faults, label='Page Faults', color='red')
    plt.bar(algorithms, hits, bottom=faults, label='Page Hits', color='green')
    plt.xlabel("Algorithms")
    plt.ylabel("Number of Pages")
    plt.title("Virtual Memory Manager Performance")
    plt.legend()
    plt.show()

def main():
    pages = list(map(int, input("Enter page reference string (space separated): ").split()))
    frame_size = int(input("Enter frame size: "))

    results = {}
    results['FIFO'] = dict(zip(['faults','hits'], fifo(pages, frame_size)))
    results['LRU'] = dict(zip(['faults','hits'], lru(pages, frame_size)))
    results['Optimal'] = dict(zip(['faults','hits'], optimal(pages, frame_size)))

    print("\nPerformance Summary:")
    for algo, data in results.items():
        print(f"{algo}: Faults = {data['faults']}, Hits = {data['hits']}, Hit Ratio = {data['hits']/len(pages):.2f}")

    plot_results(results)

if __name__ == "__main__":
    main()
