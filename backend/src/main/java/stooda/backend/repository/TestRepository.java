package stooda.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import stooda.backend.entity.Test;

public interface TestRepository extends JpaRepository<Test,Long> {
}
