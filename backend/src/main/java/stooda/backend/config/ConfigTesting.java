package stooda.backend.config;


import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import stooda.backend.entity.EducationalEntity;
import stooda.backend.entity.Test;
import stooda.backend.repository.EducationalEntityRepository;
import stooda.backend.repository.TestRepository;

import java.util.Arrays;

@Configuration
@Profile("TestingProfile")
public class ConfigTesting implements CommandLineRunner {
    @Autowired
    private EducationalEntityRepository educationalEntityRepository;

    @Autowired
    private TestRepository testRepository;

    @Override
    public void run(String... args) throws Exception {
        EducationalEntity edu1 = new EducationalEntity(null,"Liberato");
        EducationalEntity edu2 = new EducationalEntity(null,"IFSul");

        educationalEntityRepository.saveAll(Arrays.asList(edu1,edu2));

        Test test1 = new Test(null, 2024, edu1 );
        Test test2 = new Test(null, 2024, edu2 );
        Test test3 = new Test(null, 2025, edu1 );

        testRepository.saveAll(Arrays.asList(test1,test2,test3));
    }
}
