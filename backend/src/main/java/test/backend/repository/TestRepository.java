package test.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import test.backend.entity.Test;

public interface TestRepository extends JpaRepository<Test,Long> {
}
