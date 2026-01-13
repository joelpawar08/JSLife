# backend/Feature1/logic.py

import datetime
from collections import defaultdict
from typing import List, Dict, Optional

# ────────────────────────────────────────────────
# In-memory storage (replace with real DB later)
# ────────────────────────────────────────────────

problems: List[Dict] = []                     # [{id: int, title: str, link: str}]
solves: List[Dict] = []                       # [{problem_id: int, date: datetime.date}]
next_problem_id: int = 1

# Quick lookup: problem_id → problem dict
_problem_by_id: Dict[int, Dict] = {}

#Joel Pawar 
def _rebuild_problem_lookup():
    global _problem_by_id
    _problem_by_id = {p['id']: p for p in problems}


# ────────────────────────────────────────────────
# Seeding: ALL your handpicked LeetCode problems
# ────────────────────────────────────────────────

def seed_initial_problems():
    """Run once to populate the initial list of problems."""
    global next_problem_id

    if problems:  # already seeded
        return

    initial_problems = [
        # A. Array - Easy
        ("Two Sum", "https://leetcode.com/problems/two-sum/"),
        ("Best Time to Buy and Sell Stock", "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"),
        ("Remove Duplicates from Sorted Array", "https://leetcode.com/problems/remove-duplicates-from-sorted-array/"),
        ("Move Zeroes", "https://leetcode.com/problems/move-zeroes/"),
        ("Maximum Subarray", "https://leetcode.com/problems/maximum-subarray/"),
        ("Merge Sorted Array", "https://leetcode.com/problems/merge-sorted-array/"),
        ("Plus One", "https://leetcode.com/problems/plus-one/"),
        ("Contains Duplicate", "https://leetcode.com/problems/contains-duplicate/"),
        ("Intersection of Two Arrays II", "https://leetcode.com/problems/intersection-of-two-arrays-ii/"),
        ("Valid Mountain Array", "https://leetcode.com/problems/valid-mountain-array/"),

        # A. Array - Medium
        ("3Sum", "https://leetcode.com/problems/3sum/"),
        ("Container With Most Water", "https://leetcode.com/problems/container-with-most-water/"),
        ("Subarray Sum Equals K", "https://leetcode.com/problems/subarray-sum-equals-k/"),
        ("K-diff Pairs in an Array", "https://leetcode.com/problems/k-diff-pairs-in-an-array/"),
        ("Sort Colors", "https://leetcode.com/problems/sort-colors/"),
        ("Rotate Array", "https://leetcode.com/problems/rotate-array/"),
        ("Product of Array Except Self", "https://leetcode.com/problems/product-of-array-except-self/"),
        ("Find Minimum in Rotated Sorted Array", "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/"),
        ("Search in Rotated Sorted Array", "https://leetcode.com/problems/search-in-rotated-sorted-array/"),
        ("Longest Consecutive Sequence", "https://leetcode.com/problems/longest-consecutive-sequence/"),
        ("Spiral Matrix", "https://leetcode.com/problems/spiral-matrix/"),
        ("Game of Life", "https://leetcode.com/problems/game-of-life/"),
        ("Set Matrix Zeroes", "https://leetcode.com/problems/set-matrix-zeroes/"),
        ("Minimum Size Subarray Sum", "https://leetcode.com/problems/minimum-size-subarray-sum/"),
        ("Sliding Window Maximum", "https://leetcode.com/problems/sliding-window-maximum/"),
        ("Merge Intervals", "https://leetcode.com/problems/merge-intervals/"),
        ("Insert Interval", "https://leetcode.com/problems/insert-interval/"),
        ("Jump Game", "https://leetcode.com/problems/jump-game/"),
        ("Jump Game II", "https://leetcode.com/problems/jump-game-ii/"),
        ("Summary Ranges", "https://leetcode.com/problems/summary-ranges/"),

        # B. String - Easy
        ("Valid Anagram", "https://leetcode.com/problems/valid-anagram/"),
        ("Implement strStr()", "https://leetcode.com/problems/implement-strstr/"),
        ("Longest Common Prefix", "https://leetcode.com/problems/longest-common-prefix/"),
        ("Reverse String", "https://leetcode.com/problems/reverse-string/"),
        ("First Unique Character in a String", "https://leetcode.com/problems/first-unique-character-in-a-string/"),
        ("Ransom Note", "https://leetcode.com/problems/ransom-note/"),
        ("Is Subsequence", "https://leetcode.com/problems/is-subsequence/"),
        ("Count and Say", "https://leetcode.com/problems/count-and-say/"),
        ("Check If Two String Arrays are Equivalent", "https://leetcode.com/problems/check-if-two-string-arrays-are-equivalent/"),
        ("Defanging an IP Address", "https://leetcode.com/problems/defanging-an-ip-address/"),

        # B. String - Medium
        ("Longest Substring Without Repeating Characters", "https://leetcode.com/problems/longest-substring-without-repeating-characters/"),
        ("Group Anagrams", "https://leetcode.com/problems/group-anagrams/"),
        ("Valid Palindrome II", "https://leetcode.com/problems/valid-palindrome-ii/"),
        ("Longest Palindromic Substring", "https://leetcode.com/problems/longest-palindromic-substring/"),
        ("Multiply Strings", "https://leetcode.com/problems/multiply-strings/"),
        ("Decode Ways", "https://leetcode.com/problems/decode-ways/"),
        ("Integer to Roman", "https://leetcode.com/problems/integer-to-roman/"),
        ("Roman to Integer", "https://leetcode.com/problems/roman-to-integer/"),
        ("String to Integer (atoi)", "https://leetcode.com/problems/string-to-integer-atoi/"),
        ("Zigzag Conversion", "https://leetcode.com/problems/zigzag-conversion/"),
        ("Reverse Words in a String", "https://leetcode.com/problems/reverse-words-in-a-string/"),
        ("Minimum Window Substring", "https://leetcode.com/problems/minimum-window-substring/"),
        ("Find All Anagrams in a String", "https://leetcode.com/problems/find-all-anagrams-in-a-string/"),
        ("Reorganize String", "https://leetcode.com/problems/reorganize-string/"),
        ("Remove All Adjacent Duplicates in String II", "https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/"),
        ("Basic Calculator II", "https://leetcode.com/problems/basic-calculator-ii/"),
        ("Longest Repeating Character Replacement", "https://leetcode.com/problems/longest-repeating-character-replacement/"),
        ("Palindromic Substrings", "https://leetcode.com/problems/palindromic-substrings/"),
        ("Restore IP Addresses", "https://leetcode.com/problems/restore-ip-addresses/"),

        # C. Linked List - Easy
        ("Reverse Linked List", "https://leetcode.com/problems/reverse-linked-list/"),
        ("Merge Two Sorted Lists", "https://leetcode.com/problems/merge-two-sorted-lists/"),
        ("Delete Node in a Linked List", "https://leetcode.com/problems/delete-node-in-a-linked-list/"),
        ("Middle of the Linked List", "https://leetcode.com/problems/middle-of-the-linked-list/"),
        ("Linked List Cycle", "https://leetcode.com/problems/linked-list-cycle/"),
        ("Remove Linked List Elements", "https://leetcode.com/problems/remove-linked-list-elements/"),
        ("Convert Binary Number in a Linked List to Integer", "https://leetcode.com/problems/convert-binary-number-in-a-linked-list-to-integer/"),
        ("Intersection of Two Linked Lists", "https://leetcode.com/problems/intersection-of-two-linked-lists/"),
        ("Palindrome Linked List", "https://leetcode.com/problems/palindrome-linked-list/"),
        ("Design Linked List", "https://leetcode.com/problems/design-linked-list/"),

        # C. Linked List - Medium
        ("Add Two Numbers", "https://leetcode.com/problems/add-two-numbers/"),
        ("Remove Nth Node From End of List", "https://leetcode.com/problems/remove-nth-node-from-end-of-list/"),
        ("Copy List with Random Pointer", "https://leetcode.com/problems/copy-list-with-random-pointer/"),
        ("Swap Nodes in Pairs", "https://leetcode.com/problems/swap-nodes-in-pairs/"),
        ("Rotate List", "https://leetcode.com/problems/rotate-list/"),
        ("Reorder List", "https://leetcode.com/problems/reorder-list/"),
        ("Odd Even Linked List", "https://leetcode.com/problems/odd-even-linked-list/"),
        ("Reverse Nodes in k-Group", "https://leetcode.com/problems/reverse-nodes-in-k-group/"),
        ("Flatten a Multilevel Doubly Linked List", "https://leetcode.com/problems/flatten-a-multilevel-doubly-linked-list/"),
        ("Sort List", "https://leetcode.com/problems/sort-list/"),
        ("Partition List", "https://leetcode.com/problems/partition-list/"),
        ("Remove Duplicates from Sorted List II", "https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/"),
        ("Merge k Sorted Lists", "https://leetcode.com/problems/merge-k-sorted-lists/"),
        ("LRU Cache", "https://leetcode.com/problems/lru-cache/"),
        ("Intersection of Two Linked Lists II", "https://leetcode.com/problems/intersection-of-two-linked-lists/"),  # note: this is usually #160 again or variant
        ("Convert Sorted List to Binary Search Tree", "https://leetcode.com/problems/convert-sorted-list-to-binary-search-tree/"),
        ("Find the Duplicate Number", "https://leetcode.com/problems/find-the-duplicate-number/"),
        ("Linked List Cycle II", "https://leetcode.com/problems/linked-list-cycle-ii/"),
        ("Insertion Sort List", "https://leetcode.com/problems/insertion-sort-list/"),
        ("Split Linked List in Parts", "https://leetcode.com/problems/split-linked-list-in-parts/"),

        # D. Stack - Easy
        ("Valid Parentheses", "https://leetcode.com/problems/valid-parentheses/"),
        ("Min Stack", "https://leetcode.com/problems/min-stack/"),
        ("Implement Queue using Stacks", "https://leetcode.com/problems/implement-queue-using-stacks/"),
        ("Implement Stack using Queues", "https://leetcode.com/problems/implement-stack-using-queues/"),
        ("Baseball Game", "https://leetcode.com/problems/baseball-game/"),
        ("Remove All Adjacent Duplicates In String", "https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/"),
        ("Final Prices With a Special Discount in a Shop", "https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/"),
        ("Backspace String Compare", "https://leetcode.com/problems/backspace-string-compare/"),
        ("Crawler Log Folder", "https://leetcode.com/problems/crawler-log-folder/"),
        ("Make The String Great", "https://leetcode.com/problems/make-the-string-great/"),

        # D. Stack - Medium
        ("Daily Temperatures", "https://leetcode.com/problems/daily-temperatures/"),
        ("Next Greater Element II", "https://leetcode.com/problems/next-greater-element-ii/"),
        ("Asteroid Collision", "https://leetcode.com/problems/asteroid-collision/"),
        ("Evaluate Reverse Polish Notation", "https://leetcode.com/problems/evaluate-reverse-polish-notation/"),
        ("Decode String", "https://leetcode.com/problems/decode-string/"),
        ("Remove K Digits", "https://leetcode.com/problems/remove-k-digits/"),
        ("Largest Rectangle in Histogram", "https://leetcode.com/problems/largest-rectangle-in-histogram/"),
        ("Basic Calculator", "https://leetcode.com/problems/basic-calculator/"),
        ("Binary Tree Inorder Traversal", "https://leetcode.com/problems/binary-tree-inorder-traversal/"),
        ("Longest Valid Parentheses", "https://leetcode.com/problems/longest-valid-parentheses/"),
        ("Flatten Nested List Iterator", "https://leetcode.com/problems/flatten-nested-list-iterator/"),
        ("Maximal Rectangle", "https://leetcode.com/problems/maximal-rectangle/"),
        ("Score of Parentheses", "https://leetcode.com/problems/score-of-parentheses/"),
        ("Sum of Subarray Minimums", "https://leetcode.com/problems/sum-of-subarray-minimums/"),
        ("Online Stock Span", "https://leetcode.com/problems/online-stock-span/"),
        ("Simplify Path", "https://leetcode.com/problems/simplify-path/"),
        ("Car Fleet", "https://leetcode.com/problems/car-fleet/"),
        ("Minimum Add to Make Parentheses Valid", "https://leetcode.com/problems/minimum-add-to-make-parentheses-valid/"),
        ("132 Pattern", "https://leetcode.com/problems/132-pattern/"),
        ("Minimum Remove to Make Valid Parentheses", "https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/"),

        # E. Queue - Easy
        ("Implement Stack using Queues", "https://leetcode.com/problems/implement-stack-using-queues/"),
        ("Number of Recent Calls", "https://leetcode.com/problems/number-of-recent-calls/"),
        ("Moving Average from Data Stream", "https://leetcode.com/problems/moving-average-from-data-stream/"),
        ("Dota2 Senate", "https://leetcode.com/problems/dota2-senate/"),
        ("Reveal Cards In Increasing Order", "https://leetcode.com/problems/reveal-cards-in-increasing-order/"),
        ("Design Circular Queue", "https://leetcode.com/problems/design-circular-queue/"),
        ("Rotten Oranges", "https://leetcode.com/problems/rotten-oranges/"),
        ("Flood Fill", "https://leetcode.com/problems/flood-fill/"),
        ("Open the Lock", "https://leetcode.com/problems/open-the-lock/"),
        ("Binary Tree Level Order Traversal", "https://leetcode.com/problems/binary-tree-level-order-traversal/"),

        # E. Queue - Medium
        ("Perfect Squares", "https://leetcode.com/problems/perfect-squares/"),
        ("Walls and Gates", "https://leetcode.com/problems/walls-and-gates/"),
        ("Course Schedule", "https://leetcode.com/problems/course-schedule/"),
        ("Sliding Window Maximum", "https://leetcode.com/problems/sliding-window-maximum/"),
        ("Clone Graph", "https://leetcode.com/problems/clone-graph/"),
        ("Shortest Path in Binary Matrix", "https://leetcode.com/problems/shortest-path-in-binary-matrix/"),
        ("Cheapest Flights Within K Stops", "https://leetcode.com/problems/cheapest-flights-within-k-stops/"),
        ("Time Needed to Inform All Employees", "https://leetcode.com/problems/time-needed-to-inform-all-employees/"),
        ("Design Hit Counter", "https://leetcode.com/problems/design-hit-counter/"),
        ("Design Snake Game", "https://leetcode.com/problems/design-snake-game/"),
        ("Word Ladder", "https://leetcode.com/problems/word-ladder/"),
        ("Kth Largest Element in a Stream", "https://leetcode.com/problems/kth-largest-element-in-a-stream/"),
        ("The Maze", "https://leetcode.com/problems/the-maze/"),
        ("Design Twitter", "https://leetcode.com/problems/design-twitter/"),
        ("Minimum Genetic Mutation", "https://leetcode.com/problems/minimum-genetic-mutation/"),
        ("Top K Frequent Elements", "https://leetcode.com/problems/top-k-frequent-elements/"),
        ("Task Scheduler", "https://leetcode.com/problems/task-scheduler/"),
        ("Serialize and Deserialize Binary Tree", "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/"),
        ("Shortest Distance from All Buildings", "https://leetcode.com/problems/shortest-distance-from-all-buildings/"),
        ("Find the Safest Path in a Grid", "https://leetcode.com/problems/find-the-safest-path-in-a-grid/"),
    ]

    for title, link in initial_problems:
        problems.append({"id": next_problem_id, "title": title, "link": link})
        next_problem_id += 1

    _rebuild_problem_lookup()


# ────────────────────────────────────────────────
# Core Functions
# ────────────────────────────────────────────────

def add_problem(title: str, link: str) -> Dict:
    """Admin: Add a new problem."""
    global next_problem_id
    problem = {"id": next_problem_id, "title": title.strip(), "link": link.strip()}
    problems.append(problem)
    _problem_by_id[next_problem_id] = problem
    next_problem_id += 1
    return problem


def get_all_problems() -> List[Dict]:
    """Get full list with completion status."""
    solved_set = {s["problem_id"] for s in solves}
    return [
        {
            "id": p["id"],
            "title": p["title"],
            "link": p["link"],
            "completed": p["id"] in solved_set,
        }
        for p in problems
    ]


def get_problem(problem_id: int) -> Optional[Dict]:
    """Get single problem with status."""
    p = _problem_by_id.get(problem_id)
    if not p:
        return None
    solved_set = {s["problem_id"] for s in solves}
    return {
        "id": p["id"],
        "title": p["title"],
        "link": p["link"],
        "completed": p["id"] in solved_set,
    }


def mark_solved(problem_id: int) -> bool:
    """User: Mark problem as solved today (idempotent per day)."""
    if problem_id not in _problem_by_id:
        return False

    today = datetime.date.today()

    if any(s["problem_id"] == problem_id and s["date"] == today for s in solves):
        return False

    solves.append({"problem_id": problem_id, "date": today})
    return True


def get_dashboard_stats() -> Dict:
    """LeetCode-style dashboard stats - with date keys serialized to strings."""
    total = len(problems)
    solved_unique = len({s["problem_id"] for s in solves})

    daily = defaultdict(int)
    for s in solves:
        daily[s["date"]] += 1

    today = datetime.date.today()
    today_solved = daily[today]

    # Convert date → ISO string for JSON serialization
    daily_solved_serialized = {
        date_obj.isoformat(): count
        for date_obj, count in daily.items()
    }

    # Recent 7 days (also string keys)
    recent_days = {}
    for i in range(7):
        d = today - datetime.timedelta(days=i)
        recent_days[d.isoformat()] = daily[d]

    return {
        "totalProblems": total,
        "solved": solved_unique,
        "solvedPercentage": round((solved_unique / total * 100), 1) if total > 0 else 0,
        "todaySolved": today_solved,
        "dailySolved": daily_solved_serialized,
        "recent7Days": recent_days,
    }


# Auto-seed when module is imported (development convenience)
seed_initial_problems()



#then this is done and i want a really optimized system so that i can work on it where the solutions is optimized     