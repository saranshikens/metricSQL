#include "ght.h"

#include <cmath>
#include <limits>
#include <random>
#include <algorithm>

TreeNode::TreeNode(const Point& a, const Point& b)
    : pivotA(a), pivotB(b), isLeaf(false) {}

TreeNode::TreeNode(const std::vector<Point>& points)
    : bucket(points), isLeaf(true) {}

GHTIndex::GHTIndex(int leaf_size)
    : leaf_size(leaf_size) {}

float GHTIndex::distance(
    const std::vector<float>& a,
    const std::vector<float>& b
) {
    float d = 0.0f;

    for (size_t i = 0; i < a.size(); i++) {
        float diff = a[i] - b[i];
        d += diff * diff;
    }

    return std::sqrt(d);
}

void GHTIndex::build(
    const std::vector<std::vector<float>>& vectors
) {
    std::vector<Point> points;

    for (size_t i = 0; i < vectors.size(); i++) {
        points.push_back({
            static_cast<int>(i),
            vectors[i]
        });
    }

    root = build_recursive(points);
}

std::unique_ptr<TreeNode>
GHTIndex::build_recursive(
    const std::vector<Point>& points
) {
    if (points.empty()) {
        return nullptr;
    }

    if ((int)points.size() <= leaf_size) {
        return std::make_unique<TreeNode>(points);
    }

    static std::mt19937 rng(std::random_device{}());

    std::uniform_int_distribution<int> dist(
        0,
        points.size() - 1
    );

    int idA = dist(rng);
    int idB = dist(rng);

    while (idA == idB) {
        idB = dist(rng);
    }

    Point pA = points[idA];
    Point pB = points[idB];

    auto node = std::make_unique<TreeNode>(pA, pB);

    std::vector<Point> leftPartition;
    std::vector<Point> rightPartition;

    for (size_t i = 0; i < points.size(); i++) {

        if ((int)i == idA || (int)i == idB) {
            continue;
        }

        float dA = distance(points[i].coords, pA.coords);
        float dB = distance(points[i].coords, pB.coords);

        if (dA <= dB) {
            leftPartition.push_back(points[i]);
        } else {
            rightPartition.push_back(points[i]);
        }
    }

    node->left = build_recursive(leftPartition);
    node->right = build_recursive(rightPartition);

    return node;
}

void GHTIndex::search_recursive(
    TreeNode* node,
    const std::vector<float>& query,
    int& best_id,
    float& best_dist
) {
    if (!node) {
        return;
    }

    if (node->isLeaf) {

        for (const auto& point : node->bucket) {

            float d = distance(query, point.coords);

            if (d < best_dist) {
                best_dist = d;
                best_id = point.id;
            }
        }

        return;
    }

    float dA = distance(query, node->pivotA.coords);
    float dB = distance(query, node->pivotB.coords);

    if (dA < best_dist) {
        best_dist = dA;
        best_id = node->pivotA.id;
    }

    if (dB < best_dist) {
        best_dist = dB;
        best_id = node->pivotB.id;
    }

    if (dA - best_dist <= dB + best_dist) {
        search_recursive(
            node->left.get(),
            query,
            best_id,
            best_dist
        );
    }

    if (dB - best_dist <= dA + best_dist) {
        search_recursive(
            node->right.get(),
            query,
            best_id,
            best_dist
        );
    }
}

int GHTIndex::nearest_neighbor(
    const std::vector<float>& query
) {
    int best_id = -1;

    float best_dist =
        std::numeric_limits<float>::infinity();

    search_recursive(
        root.get(),
        query,
        best_id,
        best_dist
    );

    return best_id;
}

void GHTIndex::top_k_recursive(
    TreeNode* node,
    const std::vector<float>& query,
    int k,
    std::priority_queue<Neighbor>& heap
) {

    if (!node) {
        return;
    }

    auto try_insert = [&](const Point& point) {

        float d = distance(
            query,
            point.coords
        );

        if ((int)heap.size() < k) {

            heap.push({d, point.id});

        } else if (d < heap.top().distance) {

            heap.pop();

            heap.push({d, point.id});
        }
    };

    if (node->isLeaf) {

        for (const auto& point : node->bucket) {
            try_insert(point);
        }

        return;
    }

    try_insert(node->pivotA);

    try_insert(node->pivotB);

    top_k_recursive(
        node->left.get(),
        query,
        k,
        heap
    );

    top_k_recursive(
        node->right.get(),
        query,
        k,
        heap
    );
}

std::vector<int> GHTIndex::top_k_search(
    const std::vector<float>& query,
    int k
) {

    std::priority_queue<Neighbor> heap;

    top_k_recursive(
        root.get(),
        query,
        k,
        heap
    );

    std::vector<int> results;

    while (!heap.empty()) {

        results.push_back(
            heap.top().id
        );

        heap.pop();
    }

    std::reverse(
        results.begin(),
        results.end()
    );

    return results;
}