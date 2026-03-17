package stooda.backend.entity;

import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import lombok.*;

import java.io.Serializable;

@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
@EqualsAndHashCode(of = "id" )

@Entity
@Table(name = "tb_tests")
public class Test implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private int testYear;

    @ManyToOne
    @JoinColumn(name = "educationalEntity_id" )
    @JsonBackReference
    private EducationalEntity educationalEntity;
}
