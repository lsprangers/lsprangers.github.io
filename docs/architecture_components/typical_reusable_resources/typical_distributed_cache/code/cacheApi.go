package lruCache

import (
	"encoding/json"
	"net/http"
)

var svc = NewCacheWrapper(100)

func GetHandler(w http.ResponseWriter, r *http.Request) {
	key := r.URL.Query().Get("key")
	value, ok := svc.Get(key)
	if !ok {
		http.NotFound(w, r)
		return
	}
	json.NewEncoder(w).Encode(map[string]interface{}{"key": key, "value": value})
}

func PutHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Key   string      `json:"key"`
		Value interface{} `json:"value"`
	}
	json.NewDecoder(r.Body).Decode(&req)
	svc.Put(req.Key, req.Value)
	w.WriteHeader(http.StatusNoContent)
}

func main() {
	http.HandleFunc("/get", GetHandler)
	http.HandleFunc("/put", PutHandler)
	http.ListenAndServe(":8080", nil)
}
