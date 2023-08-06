#include "luxem_rawread.h"

#include "luxem_internal_common.h"

#include <assert.h>
#include <stdlib.h>
#include <stdio.h>

#if 0
#define TRACE printf("TRACE: %s\n", __func__)
#else
#define TRACE do {} while (luxem_false)
#endif

#define CONTEXT_ARGS struct luxem_rawread_context_t *context
#define CONTEXT context
#define DATA_ARGS struct luxem_string_t const *data, size_t *eaten
#define DATA data, eaten
#define STATE_ARGS CONTEXT_ARGS, DATA_ARGS, luxem_bool_t finish
#define STATE CONTEXT, DATA, finish

#define STATE_PROTO(name) \
	static enum result_t name(STATE_ARGS)

#define SET_ERROR_TARGET(message, target) \
	do { \
	target->pointer = message; \
	target->length = sizeof(message) - 1; \
	} while(0)

#define SET_ERROR(message) \
	context->error.pointer = message; \
	context->error.length = sizeof(message) - 1;

#define ERROR(message) \
	do \
	{ \
	SET_ERROR(message) \
	return result_error; \
	} while(0)

#define PUSH_STATE(state) \
	do \
	{ \
	if (!push_state(context, state)) return result_error; \
	} while(0)

enum result_t
{
	result_continue,
	result_error,
	result_hungry
};

struct luxem_rawread_buffer_t;

struct stack_t;

typedef enum result_t (*state_signature_t)(STATE_ARGS);

luxem_bool_t luxem_rawread_buffer_construct(struct luxem_rawread_buffer_t *buffer);
luxem_bool_t luxem_rawread_buffer_resize(struct luxem_rawread_buffer_t *buffer, size_t trim_front, size_t expand);
void luxem_rawread_buffer_destroy(struct luxem_rawread_buffer_t *buffer);
static luxem_bool_t call_void_callback(CONTEXT_ARGS, luxem_rawread_void_callback_t callback);
static luxem_bool_t call_string_callback(CONTEXT_ARGS, luxem_rawread_string_callback_t callback, struct luxem_string_t const *string);
static luxem_bool_t can_eat_one(DATA_ARGS);
static char taste_one(DATA_ARGS);
static char eat_one(DATA_ARGS);
static luxem_bool_t push_state(CONTEXT_ARGS, state_signature_t state);
static void remove_state(CONTEXT_ARGS, struct stack_t *node);
static luxem_bool_t is_whitespace(char const value);
static enum result_t eat_whitespace(STATE_ARGS);
STATE_PROTO(state_whitespace);
static enum result_t read_word(STATE_ARGS, struct luxem_string_t *out);
static enum result_t read_words(STATE_ARGS, char delimiter, struct luxem_string_t *out);
STATE_PROTO(state_type);
static enum result_t read_primitive(STATE_ARGS, luxem_bool_t const key);
STATE_PROTO(state_primitive);
STATE_PROTO(state_key);
STATE_PROTO(state_value_phrase);
STATE_PROTO(state_value);
static luxem_bool_t push_object_state(CONTEXT_ARGS);
STATE_PROTO(state_key_separator);
STATE_PROTO(state_object_next);
static luxem_bool_t push_array_state(CONTEXT_ARGS);
STATE_PROTO(state_array_next);

struct luxem_rawread_buffer_t
{
	size_t allocated;
	char *pointer;
};

struct stack_t
{
	state_signature_t state;
	struct stack_t *previous;
};

struct luxem_rawread_context_t
{
	struct luxem_string_t error;
	size_t eaten_absolute;
	struct stack_t *state_top;
	struct luxem_rawread_callbacks_t callbacks;
};

luxem_bool_t luxem_rawread_buffer_construct(struct luxem_rawread_buffer_t *buffer)
{
	buffer->allocated = LUXEM_BUFFER_BLOCK_SIZE * 2;
	buffer->pointer = malloc(buffer->allocated);
	return buffer->pointer == 0 ? luxem_false : luxem_true;
}

luxem_bool_t luxem_rawread_buffer_resize(struct luxem_rawread_buffer_t *buffer, size_t trim_front, size_t expand)
{
	assert(trim_front <= buffer->allocated);
	if (expand < trim_front)
	{
		memmove(buffer->pointer, buffer->pointer + trim_front, buffer->allocated - trim_front);
	}
	else
	{
		size_t new_length = buffer->allocated * 2;
		char *out = malloc(new_length);
		if (!out) 
		{
			free(buffer->pointer);
			return luxem_false;
		}
		memcpy(out, buffer->pointer + trim_front, buffer->allocated - trim_front);
		free(buffer->pointer);
		buffer->pointer = out;
		buffer->allocated = new_length;
	}
	return luxem_true;
}

void luxem_rawread_buffer_destroy(struct luxem_rawread_buffer_t *buffer)
{
	free(buffer->pointer);
}

luxem_bool_t call_void_callback(CONTEXT_ARGS, luxem_rawread_void_callback_t callback)
{
	if (callback)
		return callback(context, context->callbacks.user_data);
	return luxem_true;
}

luxem_bool_t call_string_callback(CONTEXT_ARGS, luxem_rawread_string_callback_t callback, struct luxem_string_t const *string)
{
	if (callback)
	{
		struct luxem_string_t const *unslashed = unslash(string);
		luxem_bool_t result = callback(context, context->callbacks.user_data, unslashed ? unslashed : string);
		if (unslashed) free((void *)unslashed);
		return result;
	}
	return luxem_true;
}

luxem_bool_t can_eat_one(DATA_ARGS)
{
	return *eaten < data->length;
}

char taste_one(DATA_ARGS)
{
	assert(can_eat_one(DATA));
	return data->pointer[*eaten];
}

char eat_one(DATA_ARGS)
{
	assert(can_eat_one(DATA));
	return data->pointer[(*eaten)++];
}

luxem_bool_t push_state(CONTEXT_ARGS, state_signature_t state)
{
	struct stack_t *new_top = malloc(sizeof(struct stack_t));
	if (!new_top)
	{
		SET_ERROR("Failed to malloc stack element; out of memory?");
		return luxem_false;
	}
	new_top->previous = context->state_top;
	assert(state);
	new_top->state = state;
	context->state_top = new_top;
	return luxem_true;
}

void remove_state(CONTEXT_ARGS, struct stack_t *node)
{
	struct stack_t *above = 0;
	struct stack_t *check = context->state_top;
	assert(node);
	while (check != node)
	{
		if (!check) 
		{
			assert(luxem_false);
			return;
		}
		above = check;
		check = check->previous;
	}
	if (above)
	{
		above->previous = check->previous;
	}
	else
	{
		context->state_top = check->previous;
	}
	free(check);
}

luxem_bool_t is_whitespace(char const value)
{
	switch (value)
	{
		case ' ':
		case '\t':
		case '\n':
			return luxem_true;
		default:
			return luxem_false;
	}
}

enum result_t eat_whitespace(STATE_ARGS)
{
	while (luxem_true)
	{
		if (!can_eat_one(DATA)) break;
		{
			char const next = taste_one(DATA);
			if (next == '*')
			{
				eat_one(DATA);
				if (read_words(STATE, '*', 0) == result_hungry)
					return result_hungry;
			}
			else 
			{
				if (!is_whitespace(next)) break;
				eat_one(DATA);
			}
		}
	}
	return result_continue;
}

STATE_PROTO(state_whitespace)
{
	TRACE;
	if (eat_whitespace(STATE) == result_hungry) return result_hungry;
	if (!finish && !can_eat_one(DATA)) return result_hungry;
	return result_continue;
}

enum result_t read_word(STATE_ARGS, struct luxem_string_t *out)
{
	size_t const start = *eaten;
	luxem_bool_t escaped = luxem_false;
	while (luxem_true)
	{
		if (!can_eat_one(DATA)) 
		{
			if (finish)
			{
				out->pointer = data->pointer + start;
				out->length = *eaten - start;
				return result_continue;
			}
			break;
		}
		{
			char const next = taste_one(DATA);
			if (next == '\\') 
			{
				eat_one(DATA);
				escaped = luxem_true;
			}
			else if (escaped)
			{
				eat_one(DATA);
				escaped = luxem_false;
			}
			else if (!is_word_char(next))
			{
				out->pointer = data->pointer + start;
				out->length = *eaten - start;
				return result_continue;
			}
			else eat_one(DATA);
		}
	}
	return result_hungry;
}

enum result_t read_words(STATE_ARGS, char delimiter, struct luxem_string_t *out)
{
	size_t const start = *eaten;
	luxem_bool_t escaped = luxem_false;
	while (luxem_true)
	{
		if (!can_eat_one(DATA)) break;
		{
			char const next = eat_one(DATA);
			if (next == '\\') escaped = luxem_true;
			else if (escaped) escaped = luxem_false;
			else if (next == delimiter)
			{
				if (out)
				{
					out->pointer = data->pointer + start;
					out->length = *eaten - 1 - start;
				}
				return result_continue;
			}
		}
	}
	return result_hungry;
}

STATE_PROTO(state_type)
{
	TRACE;
	{
		struct luxem_string_t type;
		enum result_t result = read_words(STATE, ')', &type);
		if (result == result_continue)
		{
			luxem_bool_t callback_result = call_string_callback(context, context->callbacks.type, &type);
			if (!callback_result) return result_error;
			return result_continue;
		}

		return result_hungry;
	}
}

enum result_t read_primitive(STATE_ARGS, luxem_bool_t const key)
{
	if (!can_eat_one(DATA)) 
	{
		if (finish)
		{
			struct luxem_string_t string;
			string.pointer = 0;
			string.length = 0;
			{
				luxem_bool_t const callback_result = 
					key ? call_string_callback(context, context->callbacks.key, &string) :
					call_string_callback(context, context->callbacks.primitive, &string);
				if (!callback_result) return result_error;
			}
			return result_continue;
		}
		else return result_hungry;
	}

	{
		struct luxem_string_t string;
		enum result_t result;
		if (taste_one(DATA) == '"')
		{
			eat_one(DATA);
			result = read_words(STATE, '"', &string);
		}
		else result = read_word(STATE, &string);
		if (result == result_continue)
		{
			luxem_bool_t const callback_result = 
				key ? call_string_callback(context, context->callbacks.key, &string) :
				call_string_callback(context, context->callbacks.primitive, &string);
			if (!callback_result) return result_error;
			return result_continue;
		}

		return result_hungry;
	}
}

STATE_PROTO(state_primitive)
{
	TRACE;
	return read_primitive(STATE, luxem_false);
}

STATE_PROTO(state_key)
{
	TRACE;
	return read_primitive(STATE, luxem_true);
}

STATE_PROTO(state_value_phrase)
{
	TRACE;
	if (!can_eat_one(DATA)) return result_hungry;
	
	PUSH_STATE(state_value);

	if (taste_one(DATA) == '(')
	{
		eat_one(DATA);
		PUSH_STATE(state_whitespace);
		PUSH_STATE(state_type);
	}

	return result_continue;
}

STATE_PROTO(state_value)
{
	TRACE;
	if (!can_eat_one(DATA)) 
	{
		if (finish)
		{
			PUSH_STATE(state_primitive);
			return result_continue;
		}
		else return result_hungry;
	}

	switch (taste_one(DATA))
	{
		case '{':
			eat_one(DATA);
			if (eat_whitespace(STATE) == result_hungry) return result_hungry;
			if (!can_eat_one(DATA)) return result_hungry;
			if (taste_one(DATA) == '}') PUSH_STATE(state_object_next);
			else { if (!push_object_state(CONTEXT)) return result_error; }
			if (!call_void_callback(context, context->callbacks.object_begin))
				return result_error;
			break;
		case '[': 
			eat_one(DATA);
			if (eat_whitespace(STATE) == result_hungry) return result_hungry;
			if (!can_eat_one(DATA)) return result_hungry;
			if (taste_one(DATA) == ']') PUSH_STATE(state_array_next);
			else { if (!push_array_state(CONTEXT)) return result_error; }
			if (!call_void_callback(context, context->callbacks.array_begin))
				return result_error;
			break;
		default: 
			PUSH_STATE(state_primitive);
			break;
	}

	return result_continue;
}

luxem_bool_t push_object_state(CONTEXT_ARGS)
{
	PUSH_STATE(state_object_next);
	PUSH_STATE(state_whitespace);
	PUSH_STATE(state_value_phrase);
	PUSH_STATE(state_whitespace);
	PUSH_STATE(state_key_separator);
	PUSH_STATE(state_whitespace);
	PUSH_STATE(state_key);
	return luxem_true;
}

STATE_PROTO(state_key_separator)
{
	TRACE;
	if (!can_eat_one(DATA)) return result_hungry;

	if (taste_one(DATA) != ':')
	{
		ERROR("Missing : between key and value.");
	}
	else eat_one(DATA);

	return result_continue;
}

STATE_PROTO(state_object_next)
{
	TRACE;
	if (!can_eat_one(DATA)) return result_hungry;

	{
		char next = taste_one(DATA);

		if ((next != ',') && (next != '}'))
		{
			ERROR("Missing , between object elements.");
		}

		if (next == ',')
		{
			eat_one(DATA);
			if (eat_whitespace(STATE) == result_hungry) return result_hungry;
			if (!can_eat_one(DATA)) return result_hungry;
			next = taste_one(DATA);
		}

		if (next == '}')
		{
			eat_one(DATA);
			if (!call_void_callback(context, context->callbacks.object_end))
				return result_error;
		}
		else { if (!push_object_state(CONTEXT)) return result_error; }

		return result_continue;
	}
}

luxem_bool_t push_array_state(CONTEXT_ARGS)
{
	PUSH_STATE(state_array_next);
	PUSH_STATE(state_whitespace);
	PUSH_STATE(state_value_phrase);
	PUSH_STATE(state_whitespace);
	return luxem_true;
}

STATE_PROTO(state_array_next)
{
	TRACE;
	if (!can_eat_one(DATA)) return result_hungry;

	{
		char next = taste_one(DATA);

		if ((next != ',') && (next != ']'))
		{
			ERROR("Missing , between array elements.");
		}

		if (next == ',')
		{
			eat_one(DATA);
			if (eat_whitespace(STATE) == result_hungry) return result_hungry;
			if (!can_eat_one(DATA)) return result_hungry;
			next = taste_one(DATA);
		}

		if (next == ']')
		{
			eat_one(DATA);
			if (!call_void_callback(context, context->callbacks.array_end))
				return result_error;
		}
		else { if (!push_array_state(CONTEXT)) return result_error; }

		return result_continue;
	}
}

struct luxem_rawread_context_t *luxem_rawread_construct(void)
{
	struct luxem_rawread_context_t *context = malloc(sizeof(struct luxem_rawread_context_t));
	
	if (!context)
	{
		return 0;
	}

	context->error.pointer = 0;
	context->error.length = 0;

	context->eaten_absolute = 0;

	context->state_top = 0;

	if (!push_array_state(context))
	{
		free(context);
		return 0;
	}

	return context;
}

void luxem_rawread_destroy(struct luxem_rawread_context_t *context)
{
	struct stack_t *top = 0;
	struct stack_t *node = context->state_top;
	while (node)
	{
		top = node;
		node = node->previous;
		free(top);
	}

	free(context);
}

struct luxem_rawread_callbacks_t *luxem_rawread_callbacks(CONTEXT_ARGS)
{
	return &context->callbacks;
}

luxem_bool_t luxem_rawread_feed(CONTEXT_ARGS, struct luxem_string_t const *data, size_t *out_eaten, luxem_bool_t finish)
{
	if (context->error.pointer) return luxem_false;
#ifndef NDEBUG
	context->error.pointer = 0;
	context->error.length = 0;
#endif
	{
		size_t eaten_data = 0;
		size_t *eaten = &eaten_data;
		while (luxem_true)
		{
			struct stack_t *node = context->state_top;

			assert(node);
			if (!node) return luxem_false;

			{
				enum result_t result = node->state(STATE);

				if (result == result_hungry) 
				{
					break;
				}

				if (result == result_error) 
				{
					assert(context->error.pointer);
					if (!context->error.pointer)
					{
						SET_ERROR("Error raised in raw callback but no error message specified.");
					}
					context->eaten_absolute += *eaten - *out_eaten;
					return luxem_false;
				}

				if (result == result_continue)
				{
					remove_state(context, node);
					if (!context->state_top)
					{
						SET_ERROR("Above root depth, exited too many levels during parsing.");
						return luxem_false;
					}
					context->eaten_absolute += *eaten - *out_eaten;
					*out_eaten = *eaten;
				}
			}
		}
	}

	return luxem_true;
}

luxem_bool_t luxem_rawread_feed_file(struct luxem_rawread_context_t *context, FILE *file, luxem_rawread_void_callback_t block_callback, luxem_rawread_void_callback_t unblock_callback)
{
	assert(file);
	{
		size_t start = 0;
		size_t stop = 0;
		struct luxem_rawread_buffer_t buffer;
		struct luxem_string_t string;

		luxem_rawread_buffer_construct(&buffer);

		while (luxem_true)
		{
			if (stop + LUXEM_BUFFER_BLOCK_SIZE > buffer.allocated)
			{
				size_t deficit = stop + LUXEM_BUFFER_BLOCK_SIZE - buffer.allocated;
				if (!luxem_rawread_buffer_resize(&buffer, start, deficit))
					return luxem_false;
				stop -= start;
				start = 0;
			}

			{
				if (block_callback) 
					block_callback(context, context->callbacks.user_data);
				{
					size_t increment = fread(buffer.pointer + stop, 1, LUXEM_BUFFER_BLOCK_SIZE, file);
					if (unblock_callback) unblock_callback(context, context->callbacks.user_data);
					{
						luxem_bool_t finish = increment == 0;
						if (finish && ferror(file))
						{
							SET_ERROR("Encountered error while reading file.");
							luxem_rawread_buffer_destroy(&buffer);
							return luxem_false;
						}

						stop += increment;

						string.pointer = buffer.pointer + start;
						string.length = stop - start;

						increment = 0;
						if (!luxem_rawread_feed(context, &string, &increment, finish))
						{
							luxem_rawread_buffer_destroy(&buffer);
							return luxem_false;
						}

						start += increment;

						if (finish)
						{
							luxem_rawread_buffer_destroy(&buffer);
							return luxem_true;
						}
					}
				}
			}
		}
	}
}

struct luxem_string_t *luxem_rawread_get_error(CONTEXT_ARGS)
{
	return &context->error;
}

size_t luxem_rawread_get_position(CONTEXT_ARGS)
{
	return context->eaten_absolute;
}

struct luxem_string_t const *luxem_from_ascii16(struct luxem_string_t const *data, struct luxem_string_t *error)
{
	assert(data);
	if (data->length % 2 != 0)
	{
		SET_ERROR_TARGET("Bad ascii16 data - length must be a multiple of 2.", error);
		return 0;
	}
	{
		size_t const new_length = data->length >> 1;
		struct luxem_string_t *out = malloc(sizeof(struct luxem_string_t) + new_length);
		if (!out) 
		{
			SET_ERROR_TARGET("Failed to allocate output memory", error);
			return 0;
		}
		out->length = data->length >> 1;
		{
			int index;
			char *cursor = (char *)out + sizeof(struct luxem_string_t);
			out->pointer = cursor;
			for (index = 0; index < new_length; ++index)
			{
				unsigned char const high = (unsigned char)data->pointer[index * 2] - (unsigned char)'a';
				unsigned char const low = (unsigned char)data->pointer[index * 2 + 1] - (unsigned char)'a';
				if ((high >= 16) ||
					(low >= 16))
				{
					SET_ERROR_TARGET("Bad ascii16 data - encountered character outside set [abcdefghijklmnop].", error);
					goto error_return;
				}
				*(cursor++) = (high << 4) + low;
			}
			assert(cursor == out->pointer + new_length);
		}
		return out;
error_return:
		free(out);
		return 0;
	}
}

