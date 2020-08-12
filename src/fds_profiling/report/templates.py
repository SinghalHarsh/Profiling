"""Contains all templates used for generating the HTML profile report"""
import jinja2

# Initializing Jinja
package_loader = jinja2.PackageLoader(
    "fds_profiling", "report/templates_structure"
)
jinja2_env = jinja2.Environment(lstrip_blocks=True, trim_blocks=True, loader=package_loader)

def template(template_name: str) -> jinja2.Template:
    """Get the template object given the name.
    Args:
      template_name: The name of the template file (.html)
    Returns:
      The jinja2 environment.
    """
    return jinja2_env.get_template(template_name)