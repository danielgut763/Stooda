package stooda.backend.service;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import stooda.backend.entity.EducationalEntity;
import stooda.backend.repository.EducationalEntityRepository;

import java.util.List;
import java.util.Optional;

@Service

public class EducationalEntityService {

    @Autowired
    private EducationalEntityRepository repository;

    public EducationalEntity create(EducationalEntity obj){
        return repository.save(obj);
    }

    public void delete(Long id){
        repository.deleteById(id);
    }

    public EducationalEntity getId(Long id){
        Optional<EducationalEntity> obj = repository.findById(id);
        return obj.get();
    }

    public List<EducationalEntity> getAll(){
        return repository.findAll();
    }

    public EducationalEntity update(EducationalEntity obj){
        Optional<EducationalEntity> newObj = repository.findById(obj.getId());
        updateEducationalEntity(newObj, obj);
        return repository.save(newObj.get());
    }

    private void updateEducationalEntity(Optional<EducationalEntity> newObj, EducationalEntity obj) {
        newObj.get().setName(obj.getName());
    }
}
