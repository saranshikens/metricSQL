#include "metric_ght.h"

#include <algorithm>
#include <limits>

MetricNode::MetricNode(
    const MetricPoint& a,
    const MetricPoint& b
)
    : pivotA(a),
      pivotB(b),
      isLeaf(false)
{
}

MetricNode::MetricNode(
    const std::vector<MetricPoint>& points
)
    : bucket(points),
      isLeaf(true)
{
}

MetricGHT::MetricGHT(
    int leaf_size
)
    : leaf_size(leaf_size)
{
}

int MetricGHT::levenshtein_distance(
    const std::string& a,
    const std::string& b
)
{
    int n = a.size();
    int m = b.size();

    std::vector<std::vector<int>> dp(
        n + 1,
        std::vector<int>(m + 1)
    );

    for (int i = 0; i <= n; i++)
        dp[i][0] = i;

    for (int j = 0; j <= m; j++)
        dp[0][j] = j;

    for (int i = 1; i <= n; i++) {

        for (int j = 1; j <= m; j++) {

            int cost =
                (a[i - 1] == b[j - 1])
                ? 0
                : 1;

            dp[i][j] = std::min({

                dp[i - 1][j] + 1,

                dp[i][j - 1] + 1,

                dp[i - 1][j - 1] + cost
            });
        }
    }

    return dp[n][m];
}

void MetricGHT::build(
    const std::vector<std::string>& values
)
{
    std::vector<MetricPoint> points;

    for (int i = 0; i < values.size(); i++) {

        points.push_back({
            i,
            values[i]
        });
    }

    root = build_recursive(points);
}

std::unique_ptr<MetricNode>
MetricGHT::build_recursive(
    const std::vector<MetricPoint>& points
)
{
    if (points.size() <= leaf_size) {

        return std::make_unique<
            MetricNode
        >(points);
    }

    MetricPoint pivotA = points[0];
    MetricPoint pivotB = points[1];

    auto node =
        std::make_unique<MetricNode>(
            pivotA,
            pivotB
        );

    std::vector<MetricPoint> left;
    std::vector<MetricPoint> right;

    for (int i = 2; i < points.size(); i++) {

        int dA =
            levenshtein_distance(
                points[i].value,
                pivotA.value
            );

        int dB =
            levenshtein_distance(
                points[i].value,
                pivotB.value
            );

        if (dA < dB)
            left.push_back(points[i]);

        else
            right.push_back(points[i]);
    }

    if (!left.empty())
        node->left =
            build_recursive(left);

    if (!right.empty())
        node->right =
            build_recursive(right);

    return node;
}

void MetricGHT::top_k_recursive(
    MetricNode* node,
    const std::string& query,
    int k,
    std::vector<
        std::pair<int,int>
    >& best
)
{
    if (!node)
        return;

    if (node->isLeaf) {

        for (const auto& point
             : node->bucket)
        {
            int d =
                levenshtein_distance(
                    query,
                    point.value
                );

            best.push_back({
                d,
                point.id
            });
        }

        return;
    }

    int dA =
        levenshtein_distance(
            query,
            node->pivotA.value
        );

    int dB =
        levenshtein_distance(
            query,
            node->pivotB.value
        );

    best.push_back({
        dA,
        node->pivotA.id
    });

    best.push_back({
        dB,
        node->pivotB.id
    });

    if (dA < dB) {

        top_k_recursive(
            node->left.get(),
            query,
            k,
            best
        );

    } else {

        top_k_recursive(
            node->right.get(),
            query,
            k,
            best
        );
    }
}

std::vector<int>
MetricGHT::top_k_search(
    const std::string& query,
    int k
)
{
    std::vector<
        std::pair<int,int>
    > best;

    top_k_recursive(
        root.get(),
        query,
        k,
        best
    );

    std::sort(
        best.begin(),
        best.end()
    );

    std::vector<int> result;

    for (
        int i = 0;
        i < std::min(
            k,
            (int)best.size()
        );
        i++
    ) {
        result.push_back(
            best[i].second
        );
    }

    return result;
}