# Scenario

You have been hired by **Refrescos Favoritos**, a fictional beverage production company, to carry out a security assessment of its industrial environment.

The company operates a production infrastructure that combines traditional IT systems with OT used to supervise and control the industrial process.

Management is concerned about the possibility that an attacker outside the organisation could compromise the corporate environment and eventually reach systems involved in production.

For this reason, you have been asked to perform the assessment from the perspective of an external attacker.

You will not be provided with direct access to the internal corporate or OT networks.

Your task is to determine whether an attacker starting outside the organisation could discover a path through the infrastructure and eventually reach the industrial control environment.

## Objective

Your objective is to perform a progressive Red Team assessment of the organisation.

Starting from the external attacker workstation, you must identify exposed services, discover vulnerabilities, obtain access to internal systems and progressively move through the environment.

The assessment should determine whether weaknesses in the organisation's security architecture could allow an external attacker to move from the Internet-facing infrastructure into the Enterprise network and eventually reach the systems responsible for monitoring and controlling the production process.

You should assume that the organisation has attempted to segment its infrastructure according to a Purdue-inspired architecture.

However, your objective is to determine whether the implemented controls are sufficient to prevent an attacker from progressing between those layers.

## Starting Conditions

You begin the exercise from an attacker workstation located outside the organisation.

At the beginning of the assessment you have no credentials and no direct access to the internal networks.

The company has only provided you with the information that one of its services is accessible from the external network.

From that point onward, all additional information must be discovered during the exercise.

You are expected to perform reconnaissance, identify potential weaknesses and use the information obtained from each system to determine your next step.

## Assessment Objectives

During the assessment, attempt to determine whether an external attacker could:

- Gain initial access to an exposed company system.
- Escalate privileges on compromised hosts.
- Discover internal network information.
- Move laterally through the Enterprise environment.
- Recover exposed credentials or sensitive configuration information.
- Identify the Industrial DMZ and its remote-access infrastructure.
- Reach systems located in the Operations and Supervision networks.
- Discover industrial communication protocols and PLC assets.
- Interact with the industrial process.
- Demonstrate the potential impact of unauthorised manipulation of process parameters.

The exercise is designed so that information discovered during one stage can provide clues required to progress to the next.

## Industrial Environment

The target organisation operates a simulated beverage production process.

The lower levels of the environment contain systems responsible for:

- Process supervision.
- Industrial data collection.
- Human-Machine Interface operation.
- Programmable Logic Controller operation.
- Mixer speed control.
- Tank-level monitoring.
- Process safety conditions.

The objective is not simply to reach these systems, but to understand how an attacker could move from an IT compromise toward an OT impact.

## Flags

Throughout the assessment you will encounter flags that confirm successful completion of different stages of the exercise.

Flags use the following format:

    flag{example_flag}

Some flags may be stored directly within compromised systems or applications.

Others may only become visible when a particular process condition is achieved.

Whenever you discover a flag, record:

- The flag value.
- The system where it was discovered.
- The action or technique that led to its discovery.

Do not assume that every flag is stored in a file.

Some flags represent successful manipulation or validation of industrial process conditions.

## Final Objective

The exercise is considered successfully completed when you can demonstrate how an attacker starting outside the organisation could progress through the environment and reach the industrial process.

Your final analysis should answer the following question:

Could an external attacker compromise the organisation's IT infrastructure, move through the IT/OT boundary and influence the industrial production process?

The purpose of the exercise is not only to obtain access, but to understand how multiple weaknesses across different architectural layers can combine into a complete attack chain.
