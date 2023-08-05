// Generated by json_to_model

#import <Foundation/Foundation.h>
{% for include in includes %}#import "{{ include.split(' ')[0] }}.h"
{% endfor %}

@interface {{ class_name }} : {{ super_name }}

- (id)initWithJSONData:(NSData *)data;
- (id)initWithJSONDictionary:(NSDictionary *)dictionary;
- (NSDictionary *)JSONDictionary;
- (NSData *)JSONData;

{% for property in properties %}
@property (nonatomic, {{ property.retain_type }}) {{ property.type }} {{ property.name }};
{% endfor %}

@end


