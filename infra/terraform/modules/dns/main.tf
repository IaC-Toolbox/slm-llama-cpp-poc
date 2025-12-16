resource "aws_route53_record" "www" {
  zone_id = var.main_zone_id
  name    = "www.viktorvasylkovskyi.com"
  type    = "A"
  alias {
    name                   = var.target_domain_name
    zone_id                = var.hosted_zone_id
    evaluate_target_health = false
  }
}