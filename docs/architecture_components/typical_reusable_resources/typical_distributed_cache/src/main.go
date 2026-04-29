package main

import (
	"encoding/json"
	"net/http"

	"lsprangers.com/cache/cache"
)

var svc = cache.NewCacheWrapper(100)

func GetHandler(w http.ResponseWriter, r *http.Request) {
	// Get "key" from URL query string - request is usually some sort of curl "http://localhost:8080/get?key=foo"
	key := r.URL.Query().Get("key")

	// Lookup value in cache
	value, ok := svc.Get(key)
	if !ok {
		http.NotFound(w, r)
		return
	}

	// Encoder looks to use http response writer to encode the return map to JSON for HTTP bytes
	json.NewEncoder(w).Encode(map[string]interface{}{"key": key, "value": value})
}

func PutHandler(w http.ResponseWriter, r *http.Request) {
	// Create a template for the request coming in
	var req struct {
		Key   string      `json:"key"`
		Value interface{} `json:"value"`
	}

	// Decode JSON from HTTP request and fill in request struct at certain memory address with data. Pass a pointer to Decode and fill in field of the var req. After this the variable req will have data filled in, if we had to handle a different request object it'd come in variables and we'd update it and pass
	json.NewDecoder(r.Body).Decode(&req)

	// Write into cache
	svc.Put(req.Key, req.Value)

	// return
	w.WriteHeader(http.StatusNoContent)
}

func HealthHandler(w http.ResponseWriter, r *http.Request) {
	// Just need to ping ponf back
	w.WriteHeader(http.StatusOK) // 200
	w.Write([]byte("OK"))
}

// curl -X POST -d '{"key":"foo","value":"bar"}' -H "Content-Type: application/json" http://localhost:8080/put
// curl "http://localhost:8080/get?key=foo"
// curl -X POST -d '{"key":"one","value":"1"}' -H "Content-Type: application/json" http://localhost:8080/put
// curl -X POST -d '{"key":"two","value":"2"}' -H "Content-Type: application/json" http://localhost:8080/put
// curl -X POST -d '{"key":"three","value":"3"}' -H "Content-Type: application/json" http://localhost:8080/put

func main() {
	http.HandleFunc("/get", GetHandler)
	http.HandleFunc("/put", PutHandler)
	http.HandleFunc("/health", HealthHandler)
	http.ListenAndServe(":8080", nil)
}
