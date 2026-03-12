package test.backend.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import test.backend.entity.Test;
import test.backend.repository.TestRepository;

import java.util.List;
import java.util.Optional;

@Service

public class TestService {

    @Autowired
    private TestRepository repository;

    public Test create(Test obj){
        return repository.save(obj);
    }

    public void delete(Long id){
        repository.deleteById(id);
    }

    public Test getId(Long id){
        Optional<Test> obj = repository.findById(id);
        return obj.get();
    }

    public List<Test> getAll(){
        return repository.findAll();
    }

    public Test update(Test obj){
        Optional<Test> newObj = repository.findById(obj.getId());
        updateTest(newObj, obj);
        return repository.save(newObj.get());
    }

    private void updateTest(Optional<Test> newObj, Test obj) {
        newObj.get().setName(obj.getName());
    }
}
