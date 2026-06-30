#pragma once

#include <string>
#include <vector>
#include <memory>

struct MetricPoint {

    int id;

    std::string value;
};

struct MetricNode {

    MetricPoint pivotA;
    MetricPoint pivotB;

    std::vector<MetricPoint> bucket;

    std::unique_ptr<MetricNode> left;
    std::unique_ptr<MetricNode> right;

    bool isLeaf;

    MetricNode(
        const MetricPoint& a,
        const MetricPoint& b
    );

    MetricNode(
        const std::vector<MetricPoint>& points
    );
};

class MetricGHT {

public:

    MetricGHT(
        int leaf_size = 4
    );

    void build(
        const std::vector<std::string>& values
    );

    std::vector<int> top_k_search(
        const std::string& query,
        int k
    );

private:

    std::unique_ptr<MetricNode> root;

    int leaf_size;

    int levenshtein_distance(
        const std::string& a,
        const std::string& b
    );

    std::unique_ptr<MetricNode>
    build_recursive(
        const std::vector<MetricPoint>& points
    );

    void top_k_recursive(
        MetricNode* node,
        const std::string& query,
        int k,
        std::vector<
            std::pair<int,int>
        >& best
    );
};