#include <linux/build-salt.h>
#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(.gnu.linkonce.this_module) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section(__versions) = {
	{ 0xc6edef59, "module_layout" },
	{ 0x79b606c4, "single_release" },
	{ 0x933faf0, "seq_lseek" },
	{ 0xc57aa0b8, "remove_proc_entry" },
	{ 0xbe8a9f60, "proc_create_data" },
	{ 0xd6ee688f, "vmalloc" },
	{ 0xc5850110, "printk" },
	{ 0x1e35ea9c, "single_open" },
	{ 0xda9f3755, "PDE_DATA" },
	{ 0xbdfb6dbb, "__fentry__" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "3499AD071378A48C7E08AD2");
