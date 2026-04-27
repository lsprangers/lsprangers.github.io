// Package btree implements a B-tree data structure.
//
// A B-tree is a self-balancing tree data structure that maintains sorted data
// and allows searches, sequential access, insertions, and deletions in logarithmic time.
//
// This implementation supports:
//   - Configurable tree order
//   - Automatic node splitting with cascade
//   - Multi-level tree structure
//
// Example usage:
//
//	bt := btree.NewBTree(3)
//	bt.Insert(10, "value_10")
//	value, found := bt.Search(10)
package btree

import (
	"fmt"
	"sort"
)

// restricts to key types that can be ordered (numbers + strings)
type Ordered interface {
	~int | ~int8 | ~int16 | ~int32 | ~int64 |
		~uint | ~uint8 | ~uint16 | ~uint32 | ~uint64 |
		~float32 | ~float64 | ~string
}

// Interface for types that support both Search and Insert where:
//
//	K: is anything in Ordered Interface
//	V: Is any generic value that can be stored and looked-up / equated
type TreeSearcher[K Ordered, V any] interface {
	Search(key K) (V, bool)
	Insert(key K, value V) error
}

// Node is a structure with keys, values, and pointers
// to other nodes, along with a pointer back to it's parent
type Node[K Ordered, V any] struct {
	keys     []K
	values   []V
	children []*Node[K, V]
	parent   *Node[K, V]
	isLeaf   bool
}

// String representation of a Node
func (n *Node[K, V]) String() string {
	nodeType := "Internal"
	if n.isLeaf {
		nodeType = "Leaf"
	}
	var pairs []string
	for i := 0; i < len(n.keys); i++ {
		pairs = append(pairs, fmt.Sprintf("%v", n.keys[i]))
	}
	return fmt.Sprintf("[%s %v]", nodeType, pairs)
}

// BTree represents a B-tree data structure with a configurable order
// Order determines the maximum number of keys per node
type BTree[K Ordered, V any] struct {
	root  *Node[K, V]
	order int
}

// String representation of a BTree, which does String print (sprint)
func (bt *BTree[K, V]) String() string {
	if bt.root == nil || len(bt.root.keys) == 0 {
		return fmt.Sprintf("BTree(order=%d) <empty>", bt.order)
	}
	var result string
	result = fmt.Sprintf("BTree(order=%d)\n", bt.order)
	result += bt.formatNode(bt.root, "", true)
	return result
}

// Another string representation of node connections
func (bt *BTree[K, V]) formatNode(n *Node[K, V], prefix string, isLast bool) string {
	var result string
	connector := "├── "
	if isLast {
		connector = "└── "
	}

	result += prefix + connector + n.String() + "\n"

	childPrefix := prefix
	if isLast {
		childPrefix += "    "
	} else {
		childPrefix += "│   "
	}

	for i, child := range n.children {
		isLastChild := i == len(n.children)-1
		result += bt.formatNode(child, childPrefix, isLastChild)
	}

	return result
}

// & is the address of operator, which is a pointer to a variable
// * is dereference operator like in Cpp, which allows access
// to the variable at that pointer location
// This returns a pointer to BTree, and returns address
func NewBTree[K Ordered, V any](order int) *BTree[K, V] {
	// memory of this Node itself
	root := &Node[K, V]{
		keys:   make([]K, 0),
		values: make([]V, 0),
		isLeaf: true,
	}
	// return pointer to BTree starting at root
	return &BTree[K, V]{
		root:  root,
		order: order,
	}
}

// returns both the value of type V and bool indicating if it
// was found of not
func (bt *BTree[K, V]) Search(key K) (V, bool) {
	if bt.root == nil || len(bt.root.keys) == 0 {
		return *new(V), false
	}
	return bt.searchNode(bt.root, key)
}

// Insert adds a key-value pair to the B-tree
// Returns an error if the key already exists
func (bt *BTree[K, V]) Insert(key K, value V) error {
	return bt.insert(bt.root, key, value)
}

func (bt *BTree[K, V]) insert(n *Node[K, V], key K, value V) error {
	if len(n.keys) == 0 {
		appendToNode(n, key, value)
		return nil
	}

	// find first valid X greater than insertion
	idx := sort.Search(len(n.keys), func(i int) bool {
		return n.keys[i] >= key
	})
	if idx < len(n.keys) && n.keys[idx] == key {
		return fmt.Errorf("key %v already exists", key)
	}

	// Once found, insert into specific node
	targetNode, err := bt.insertInNode(n, key, value, idx)
	if err != nil {
		return err
	}
	// Split if full
	if len(targetNode.keys) > bt.order {
		bt.handleOverflow(targetNode)
	}
	return nil
}

func (bt *BTree[K, V]) insertInNode(n *Node[K, V], key K, value V, idx int) (*Node[K, V], error) {
	if !n.isLeaf {
		targetNode := n.children[idx]
		err := bt.insert(targetNode, key, value)
		if err != nil {
			return nil, err
		}
		return targetNode, nil
	}
	if idx == len(n.keys) {
		appendToNode(n, key, value)
	} else {
		n.keys = insertAtIndex(n.keys, key, idx)
		n.values = insertAtIndex(n.values, value, idx)
	}

	return n, nil
}

// Once a node is too large, find median, create new 2 nodes, and split
// the node into 2
func (bt *BTree[K, V]) handleOverflow(targetNode *Node[K, V]) {
	key, value, newNode := bt.split(targetNode)
	if targetNode == bt.root {
		bt.createNewRoot(targetNode, newNode, key, value)
		return
	}
	bt.insertPromotedKey(targetNode.parent, newNode, key, value)
}

func (bt *BTree[K, V]) insertPromotedKey(parent *Node[K, V], newChild *Node[K, V], key K, value V) {
	newChild.parent = parent

	idx := sort.Search(len(parent.keys), func(i int) bool {
		return parent.keys[i] >= key
	})

	parent.children = insertAtIndex(parent.children, newChild, idx+1)

	parent.keys = insertAtIndex(parent.keys, key, idx)
	parent.values = insertAtIndex(parent.values, value, idx)
	if len(parent.keys) > bt.order {
		bt.handleOverflow(parent)
	}

}

func (bt *BTree[K, V]) createNewRoot(targetNode, newNode *Node[K, V], key K, value V) {
	bt.root = &Node[K, V]{
		keys:     append([]K{}, key),
		values:   append([]V{}, value),
		children: []*Node[K, V]{targetNode, newNode},
		parent:   nil,
		isLeaf:   false,
	}
	newNode.parent = bt.root
	targetNode.parent = bt.root
}

func (bt *BTree[K, V]) split(n *Node[K, V]) (K, V, *Node[K, V]) {
	medianIdx := len(n.keys) / 2
	medianKey := n.keys[medianIdx]
	medianValue := n.values[medianIdx]

	rightChild := Node[K, V]{
		children: make([]*Node[K, V], 0),
		isLeaf:   n.isLeaf,
		keys:     make([]K, 0),
		values:   make([]V, 0),
	}
	if medianIdx < len(n.keys)-1 {
		// ... here is Go variadic argument operator, which means
		// to expand the slice into individual elements
		//
		// It basically is saying add things one-by-one for everything after medianIdx + 1
		// instead of adding things as an entirely whole slice
		rightChild.keys = append([]K{}, n.keys[medianIdx+1:]...)
		rightChild.values = append([]V{}, n.values[medianIdx+1:]...)
		if !n.isLeaf {
			rightChild.children = append(rightChild.children, n.children[medianIdx+1:]...)
			n.children = n.children[:medianIdx+1]
			for _, child := range n.children {
				child.parent = n
			}
			for _, child := range rightChild.children {
				child.parent = &rightChild
			}
		}
	}

	n.keys = append([]K{}, n.keys[:medianIdx]...)
	n.values = append([]V{}, n.values[:medianIdx]...)

	return medianKey, medianValue, &rightChild
}

func appendToNode[K Ordered, V any](n *Node[K, V], key K, value V) {
	n.keys = append(n.keys, key)
	n.values = append(n.values, value)
}

func insertAtIndex[V any](arr []V, value V, idx int) []V {
	arr = append(arr, *new(V)) // Add space
	copy(arr[idx+1:], arr[idx:])
	arr[idx] = value
	return arr
}

// Recursively searches for a key in a BTree node and it's children
func (bt *BTree[K, V]) searchNode(n *Node[K, V], key K) (V, bool) {
	// find the smallest index where n.keys[idx] >= key
	// sort.Search returns first valid X. It's passed
	// the size len(n.keys), and the comparison lambda function
	idx := sort.Search(len(n.keys), func(i int) bool {
		return n.keys[i] >= key
	})

	// if a value is actually found
	if idx < len(n.keys) && n.keys[idx] == key {
		return n.values[idx], true
	}

	// if it's not found, then continue searching if we're not at a leaf
	if !n.isLeaf {
		// n.children[idx] represents the child node at [idx] which represents
		// the immediate left value of where idx would be placed if it was there
		// which represents all keys less than n.keys[idx]
		return bt.searchNode(n.children[idx], key)
	}

	// if it's not found, and we're at a leaf
	return *new(V), false
}
