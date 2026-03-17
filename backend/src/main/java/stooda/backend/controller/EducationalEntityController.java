package stooda.backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import stooda.backend.entity.EducationalEntity;
import stooda.backend.service.EducationalEntityService;

import java.util.List;

@RestController
@RequestMapping(value = "/educationalEntity")
public class EducationalEntityController {
    @Autowired
    private EducationalEntityService service;

    @PostMapping
    public ResponseEntity<EducationalEntity> create(@RequestBody EducationalEntity obj){
        return ResponseEntity.status(HttpStatus.CREATED).body(service.create(obj));
    }

    @DeleteMapping(value = "/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id){
        service.delete(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping(value = "/{id}")
    public ResponseEntity<EducationalEntity> getId(@PathVariable Long id){
        return ResponseEntity.ok().body(service.getId(id));
    }

    @GetMapping
    public ResponseEntity<List<EducationalEntity>> getAll(){
        return ResponseEntity.ok().body(service.getAll());
    }

    @PutMapping(value = "/{id}")
    public ResponseEntity<EducationalEntity> update(@PathVariable Long id, @RequestBody EducationalEntity obj){
        obj.setId(id);
        return ResponseEntity.ok().body(service.update(obj));
    }
}
