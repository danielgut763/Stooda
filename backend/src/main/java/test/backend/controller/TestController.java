package test.backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import test.backend.entity.Test;
import test.backend.service.TestService;

import java.util.List;

@RestController
@RequestMapping(value = "/tests")
public class TestController {
    @Autowired
    private TestService service;

    @PostMapping
    public ResponseEntity<Test> create(@RequestBody Test obj){
        return ResponseEntity.status(HttpStatus.CREATED).body(service.create(obj));
    }

    @DeleteMapping(value = "/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id){
        service.delete(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping(value = "/{id}")
    public ResponseEntity<Test> getId(@PathVariable Long id){
        return ResponseEntity.ok().body(service.getId(id));
    }

    @GetMapping
    public ResponseEntity<List<Test>> getAll(){
        return ResponseEntity.ok().body(service.getAll());
    }

    @PutMapping(value = "/{id}")
    public ResponseEntity<Test> update(@PathVariable Long id, @RequestBody Test obj){
        obj.setId(id);
        return ResponseEntity.ok().body(service.update(obj));
    }
}
