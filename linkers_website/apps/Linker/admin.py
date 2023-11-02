import json
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Linker, flexibility, Hydrophobicity

#register the models/databases
@admin.register(Linker)
@admin.register(flexibility)
class LinkerResource(ImportExportModelAdmin):
    pass

@admin.register(Hydrophobicity)
class HydrophobicityAdmin(admin.ModelAdmin):
    actions = ['import_data']

    def import_data(self, request, queryset):
        with open('linkers_website/data/hydrophobicity_data.json', 'r') as json_file:
            data = json.load(json_file)

            for item in data:
                acidic_img_data = item['hydrophobicity_image']['acidic']
                neutral_img_data = item['hydrophobicity_image']['neutral']

                # Get the existing record if it exists
                existing_record, created = Hydrophobicity.objects.get_or_create(
                    id=item['id'],
                    defaults={
                        'sequence': item['sequence'],
                        'acidic_very_hydrophobic': item['hydrophobicity_calc']['acidic'].get('Very Hydrophobic', 0.0),
                        'acidic_hydrophobic': item['hydrophobicity_calc']['acidic'].get('Hydrophobic', 0.0),
                        'acidic_neutral': item['hydrophobicity_calc']['acidic'].get('Neutral', 0.0),
                        'acidic_hydrophilic': item['hydrophobicity_calc']['acidic'].get('Hydrophilic', 0.0),
                        'neutral_very_hydrophobic': item['hydrophobicity_calc']['neutral'].get('Very Hydrophobic', 0.0),
                        'neutral_hydrophobic': item['hydrophobicity_calc']['neutral'].get('Hydrophobic', 0.0),
                        'neutral_neutral': item['hydrophobicity_calc']['neutral'].get('Neutral', 0.0),
                        'neutral_hydrophilic': item['hydrophobicity_calc']['neutral'].get('Hydrophilic', 0.0),
                        'gravy_score': item['gravy_score'],
                        
                    }
                )

                # Update the record with the new values from the JSON file
                existing_record.sequence = item['sequence']
                existing_record.acidic_very_hydrophobic = item['hydrophobicity_calc']['acidic'].get('Very Hydrophobic', 0.0)
                existing_record.acidic_hydrophobic = item['hydrophobicity_calc']['acidic'].get('Hydrophobic', 0.0)
                existing_record.acidic_neutral = item['hydrophobicity_calc']['acidic'].get('Neutral', 0.0)
                existing_record.acidic_hydrophilic = item['hydrophobicity_calc']['acidic'].get('Hydrophilic', 0.0)
                existing_record.neutral_very_hydrophobic = item['hydrophobicity_calc']['neutral'].get('Very Hydrophobic', 0.0)
                existing_record.neutral_hydrophobic = item['hydrophobicity_calc']['neutral'].get('Hydrophobic', 0.0)
                existing_record.neutral_neutral = item['hydrophobicity_calc']['neutral'].get('Neutral', 0.0)
                existing_record.neutral_hydrophilic = item['hydrophobicity_calc']['neutral'].get('Hydrophilic', 0.0)
                existing_record.gravy_score = item['gravy_score']
                

                # Check if the img data is missing and update it only if it exists in the JSON
                if acidic_img_data:
                    existing_record.acidic_img_data = acidic_img_data
                if neutral_img_data:
                    existing_record.neutral_img_data = neutral_img_data

                # Save the updated record
                existing_record.save()

        self.message_user(request, "Data imported successfully.")


    import_data.short_description = "Import data from hydrophobicity_data.json"
