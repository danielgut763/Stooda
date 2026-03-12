package test.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import test.backend.entity.Test;

public interface TestReposiory extends JpaRepository<Test,Long> {
}
