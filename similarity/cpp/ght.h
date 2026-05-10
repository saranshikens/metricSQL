#pragma once

#include <vector>
#include <memory>
#include <queue>

struct Point {
    int id;
    std::vector<float> coords;
};

struct Neighbor {

    float distance;
    int id;

    bool operator<(const Neighbor& other) const {
        return distance < other.distance;
    }
};

struct TreeNode {

    Point pivotA;
    Point pivotB;

    std::vector<Point> bucket;

    std::unique_ptr<TreeNode> left;
    std::unique_ptr<TreeNode> right;

    bool isLeaf;

    TreeNode(const Point& a, const Point& b);

    TreeNode(const std::vector<Point>& points);
};

class GHTIndex {

public:

    GHTIndex(int leaf_size = 4);

    void build(
        const std::vector<std::vector<float>>& vectors
    );

    int nearest_neighbor(
        const std::vector<float>& query
    );

    std::vector<int> top_k_search(
        const std::vector<float>& query,
        int k
    );

private:

    std::unique_ptr<TreeNode> root;

    int leaf_size;

    float distance(
        const std::vector<float>& a,
        const std::vector<float>& b
    );

    std::unique_ptr<TreeNode> build_recursive(
        const std::vector<Point>& points
    );

    void search_recursive(
        TreeNode* node,
        const std::vector<float>& query,
        int& best_id,
        float& best_dist
    );

    void top_k_recursive(
        TreeNode* node,
        const std::vector<float>& query,
        int k,
        std::priority_queue<Neighbor>& heap
    );
};