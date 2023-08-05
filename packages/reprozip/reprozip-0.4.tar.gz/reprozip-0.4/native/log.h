#ifndef LOG_H
#define LOG_H

#include <stdio.h>
#include <time.h>

#include <sys/time.h>
#include <sys/types.h>


void log_real_(pid_t tid, const char *tag, const char *format, ...);


#ifdef __GNUC__

#define log_critical(i, s, ...) log_critical_(i, s "\n", ## __VA_ARGS__)
#define log_error(i, s, ...) log_critical_(i, s "\n", ## __VA_ARGS__)
#define log_warn(i, s, ...) log_warn_(i, s "\n", ## __VA_ARGS__)
#define log_info(i, s, ...) log_info_(i, s "\n", ## __VA_ARGS__)

#define log_critical_(i, s, ...) log_real_(i, "CRITICAL", s, ## __VA_ARGS__)
#define log_error_(i, s, ...) log_real_(i, "ERROR", s, ## __VA_ARGS__)
#define log_warn_(i, s, ...) log_real_(i, "WARNING", s, ## __VA_ARGS__)
#define log_info_(i, s, ...) log_real_(i, "INFO", s, ## __VA_ARGS__)

#else

#define log_critical(i, s, ...) log_critical_(i, s "\n", __VA_ARGS__)
#define log_error(i, s, ...) log_critical_(i, s "\n", __VA_ARGS__)
#define log_warn(i, s, ...) log_warn_(i, s "\n", __VA_ARGS__)
#define log_info(i, s, ...) log_info_(i, s "\n", __VA_ARGS__)

#define log_critical_(i, s, ...) log_real_(i, "CRITICAL", s, __VA_ARGS__)
#define log_error_(i, s, ...) log_real_(i, "ERROR", s, __VA_ARGS__)
#define log_warn_(i, s, ...) log_real_(i, "WARNING", s, __VA_ARGS__)
#define log_info_(i, s, ...) log_real_(i, "INFO", s, __VA_ARGS__)
#endif

#endif
